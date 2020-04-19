<template>
  <div class="mask">
    <div class="stop-card">
      <div class="l1">
        <div class="stop-name">{{info.stopInfo.stopName}}</div>
        <div class="direction">开往：{{info.direction}}</div>
      </div>
      <div class="next-info" @click="$emit('update', info)">
        <span class="txt">下一班：</span>
        <div class="time-left">{{timeLeft}}</div>
        <div class="other-left" v-if="info.status === 'running'">
          <span class="stop-left">剩余 <span class="color">{{info.left.stopInterval || 0}}</span> 站</span>
          <span class="distance-left">约 <span class="color">{{info.left.distance || 0}}</span> 米</span>
        </div>
      </div>
      <div class="watch-btn" v-if="!isWatching" @click="watch()">关注本站</div>
      <div class="watch-btn" v-if="isWatching" @click="cancelWatch()">取消关注</div>
      <div class="close" @click="$emit('close')"></div>
    </div>
  </div>
</template>

<script>
function slice2(str) {
  return ('0' + str).slice(-2)
}
import store from '../store.js'
export default {
  props: ['info'],
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  computed: {
    timeLeft() {
      if (this.info.status === 'waiting') return '等待发车'
      return `${slice2(Math.floor(this.info.left.time / 60))}:${slice2(this.info.left.time % 60)}`
    },
    isWatching() {
      return (store.watchList.some(v => v.router === this.info.router && v.stopInfo.stopId === this.info.stopInfo.stopId && v.direction === this.info.direction))
    }
  },
  methods: {
    watch() {
      store.watchNew(this.info)
      this.$emit('close')
      this.$toast.bottom('已关注，请在首页查看！')
    },
    cancelWatch() {
      store.cancelWatch(this.info)
      this.$emit('close')
      this.$toast.bottom('已取消！')
      this.$emit('cancelWatch', this.info)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .mask {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.6);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .stop-card {
    transform: translateY(-.2rem);
    width: 3rem;
    height: 2rem;
    background: #fff;
    border-radius: 3px;
    padding: .1rem;
  }
  .l1 {
    display: flex;
    justify-content: space-between;
  }
  .direction {
    font-size: .12rem;
    color: #aaa;
  }
  .next-info {
    width: 1.5rem;
    height: 1rem;
    margin: .2rem auto;
    border: solid 1px #1abc9c;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
  }
  .next-info>div {
    width: 100%;
    text-align: center;
  }
  .txt {
    position: absolute;
    top: .05rem;
    left: .05rem;
    font-size: .12rem;
    color: #aaa;
  }
  .time-left {
    font-weight: bold;
    color: #1abc9c;
    font-size: .18rem; 
    transform: translateY(.1rem);
  }
  .other-left {
    font-size: .14rem;
    color: #666;
    transform: translateY(-.1rem);
  }
  .watch-btn {
    background: #1abc9c;
    line-height: .35rem;
    color: #fff;
    width: 1.5rem;
    border-radius: .03rem;
    margin: 0 auto;
    text-align: center;
  }
  .color {
    color: #1abc9c;
  }
  .close {
    width: .4rem;
    height: .4rem;
    position: absolute;
    left: 50%;
    bottom: 0;
    transform: translate(-50%, 1rem);
    background-image: url(assets/icons8-cancel-50.png);
    background-size: cover;
  }
</style>
