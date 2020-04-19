<template>
  <div class="page-container">
    <pageHeader :showBack="false">
      <div class="help" slot="rightIcon" @click="$router.push('/help')"></div>
    </pageHeader>
    <div class="page-body">
      <div class="list">
        <div :class="{item: true, 'is-running': item.isRunning}" v-for="(item, i) in watchList" @click="showStopInfoCard(item)" :key="i">
          <div class="bus">{{item.router}}</div>
          <div class="detail">
            <div :class="['direction', 'direction-' + item.directionNo]">开往：{{item.direction}}</div>
            <div class="station">{{item.stopInfo.stopName}}</div>
          </div>
          <div class="right" @click.stop="run(item)">
            <div class="clock"></div>
            <div class="time">
              <span v-if="item.status === 'waiting'">等待发车</span>
              <span v-else>{{`${slice2(Math.floor(item.left.time / 60))}:${slice2(item.left.time % 60)}`}}</span>
            </div>
          </div>
        </div>
        <div class="empty"  v-if="!watchList.length">
          <div class="empty-text">暂无关注中的公交站点</div>
          <div class="empty-add" @click="goSearch()">立即添加</div>
        </div>
      </div>
      <div class="add" v-if="watchList.length" @click="goSearch()">＋</div>
      <div data-clipboard-text="http://voice_bus.puzhibaike.com" class="copy-btn">点击复制下载链接，分享给好友</div>
      <div class="notice" v-if="notice" v-html="notice" @click="notice = null"></div>
    </div>
    <stopInfoCard v-if="stopInfo" :info="stopInfo" @update="updateStop" @close="stopInfo=null" @cancelWatch="cancelWatchHandler"></stopInfoCard>
  </div>
</template>

<script>
import pageHeader from '../components/header.vue'
import stopInfoCard from '../components/stopInfo.vue'
import {request} from '../util/index.js'
import store from '../store.js'
import clipboard from 'clipboard'
function delay(ms) {
  var fnQueue = []
  setInterval(function() {
    if (fnQueue[0]) {
      fnQueue.shift()()
    }
  }, ms)
  return function(fn) {
    var context = this
    return function() {
      var args = arguments
      function a() {
        fn.apply(context, args)
      }
      setTimeout(function() {
        window.plus.device.beep(1)
      }, 3000)
      fnQueue.push(a)
    }
  }
}
export default {
  data () {
    return {
      notice: '',
      version: '1.0.2',
      stopInfo: null,
      playInOrder: delay(5000)
    }
  },
  components: {
    pageHeader,
    stopInfoCard
  },
  async created() {
    this.initWatchList()
    this.notice = (await this.getNotice()).data.text
  },
  mounted() {
    var c = new clipboard('.copy-btn')
    c.on('success', function(e) {
      window.alert('复制成功！')
    });
  },
  methods: {
    async getNotice() {
      return await request('bus/get_notice')
    },
    run(item) {
      if (!item.isRunning && this.watchList.filter(v => v.isRunning).length >= 2) {
        this.$toast.bottom('最多仅可同时监控两条公交线路！')
        return
      }
      item.isRunning = !item.isRunning
      if (item.isRunning && !item.interval) {
        item.interval = setInterval(() => {
          this.updateStop(item, true)
        }, 1000 * 60)
      } else {
        clearInterval(item.interval)
        item.interval = null
      }
      store.refreshWatchList(this.watchList)
    },
    updateStop(item, playAudio) {
      request('bus/<router_name>/stop/<stop_id>',
        {
          router_name: item.router,
          stop_id: item.stopInfo.stopId
        },
        {
          direction: item.directionNo
        }
      ).then(r => {
        item.left.time = r.data.time
        item.left.distance = r.data.distance
        item.left.stopInterval = r.data.stop_interval
        item.status = r.data.status
        store.refreshWatchList(this.watchList)
        if (playAudio) {
          this.playInOrder(this.playAudio)(item, r)
        }
      })
    },
    goSearch() {
      this.$router.push({
        path: 'search'
      })
    },
    showStopInfoCard(item) {
      this.$loading()
      request('bus/<router_name>/stop/<stop_id>',
        {
          router_name: item.router,
          stop_id: item.stopInfo.stopId
        },
        {
          direction: item.directionNo
        }
      ).then(r => {
        item.left.time = r.data.time
        item.left.distance = r.data.distance
        item.left.stopInterval = r.data.stop_interval
        item.status = r.data.status
        this.stopInfo = item
        this.$loading.close()
      })
    },
    initWatchList() {
      this.watchList.forEach((item, i) => {
        item.left.time = 0
        if (item.interval) {
          clearInterval(item.interval)
          item.interval = null
        }
        if (item.isRunning && !item.interval) {
          this.updateStop(item)
          item.interval = setInterval(() => {
            this.updateStop(item, true)
          }, 1000 * 60)
        }
      })
    },
    playAudio(item, r) {
      var url = 'http://voice_bus.puzhibaike.com/api/voice/bus/<router_name>/minutes/<minutes>'
      var minutes
      if (r.data.status === 'waiting') {
        minutes = 'waiting'
      } else if (Math.round(r.data.time / 60) === 0) {
        minutes = 'soon'
      } else {
        minutes = Math.round(r.data.time / 60)
      }
      var params = {
        router_name: item.router,
        minutes
      }
      Object.keys(params).forEach(p => {
        url = url.replace(new RegExp('<' + p + '>', 'ig'), params[p])
      })
      audio.src = url
      audio.play()
    },
    cancelWatchHandler(item) {
      if (item && item.interval) {
        clearInterval(item.interval)
        item.interval = null
      }
    },
    slice2(str) {
      return ('0' + str).slice(-2)
    }
  },
  watch: {
  },
  computed: {
    watchList() {
      return store.watchList
    }
  }
}
</script>
<style scoped>
  .help {
    background: url(assets/help.png);
    background-size: cover;
    height: 100%;
    width: 100%;
  }
  .empty {
    margin-top: 50%;
  }
  .empty-text {
    font-size: .14rem;
    margin-bottom: .1rem;
    color: #666;
    text-align: center;
  }
  .empty-add {
    width: 1.2rem;
    line-height: .35rem;
    color: #fff;
    text-align: center;
    font-size: .16rem;
    margin: 0 auto;
    background: #1abc9c;
    border-radius: .5rem;
  }
  .item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #fff;
    color: #666;
    padding: .1rem 0;
    margin-bottom: 10px;
  }
  .item.is-running .time {
    display: block;
    color: #1abc9c;
  }
  .item.is-running .clock {
    background-image: url('./clock.png');
  }
  .bus {
    width: .8rem;
    text-align: center;
  }
  .detail {
    border: solid 1px #eee;
    border-width: 0 1px;
    padding: 0 10px;
    flex-grow: 1;
  }
  .direction {
    font-size: .12rem;
    padding: .05rem 0;
    padding-top: .12rem;
  }
  .direction-0 {
    background: url(assets/direction-0.png) no-repeat;
  }
  .direction-1 {
    background: url(assets/direction-1.png) no-repeat;
  }
  .right {
    text-align: center;
    width: .6rem;
  }
  .time {
    font-size: .12rem;
    color: #bbb;
  }
  .clock {
    width: .6rem;
    background-image: url('./clock-gray.png');
    height: .3rem;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
  }
  .add {
    display: flex;
    width: 0.5rem;
    height: 0.5rem;
    border-radius: .5rem;
    justify-content: center;
    align-items: center;
    font-size: .5rem;
    color: #fff;
    background: #1abc9c;
    position: fixed;
    right: .2rem;
    bottom: .2rem;
  }
  .copy-btn {
    position: fixed;
    width: 100%;
    bottom: 0;
    line-height: 3;
    text-align: center;
    color: blue;
    font-size: 14px;
  }
  .notice {
    position: fixed;
    width: 100%;
    top: .49rem;
    line-height: 3;
    text-align: center;
    color: blue;
    font-size: 14px;
    color: #fff;
    background: orange;
  }
</style>
