<template>
	<div class="page-container">
    <pageHeader :title="$route.query.router"></pageHeader>
    <div class="page-body" v-if="details">
      <div class="direction">
        <div class="left">
          <span>{{details.from}}</span> → <span>{{details.to}}</span>
        </div>
        <div class="exchange" @click="getDetail()"></div>
      </div>
      <div class="detail-list">
        <div class="item" v-for="(item, i) in details.stops" :key="i" @click="getStop(item)">{{i + 1}}. {{item.stop_name}}</div>
      </div>
      <stopInfoCard v-if="stopInfo" :info="stopInfo" @close="stopInfo=null"></stopInfoCard>
    </div>
  </div>
</template>
<script type="text/javascript">
import {request} from '../util/index.js'
import pageHeader from '../components/header.vue'
import stopInfoCard from '../components/stopInfo.vue'
export default {
  data () {
    return {
      direction: 1,
      details: null,
      stopInfo: null
    }
  },
  components: {
    pageHeader,
    stopInfoCard
  },
  created() {
    this.getDetail()
  },
  methods: {
    getDetail() {
      this.$loading('正在查询')
      this.direction = Number(!this.direction)
      request('bus/<router_name>',
        {
          router_name: this.$route.query.router
        },
        {
          direction: this.direction
        }
      ).then(r => {
        this.details = r.data
        this.$loading.close()
      })
    },
    getStop(item) {
      this.$loading('正在查询')
      request('bus/<router_name>/stop/<stop_id>',
        {
          router_name: this.$route.query.router,
          stop_id: item.stop_id
        },
        {
          direction: this.direction
        }
      ).then(r => {
        this.stopInfo = r.data
        this.stopInfo = {
          status: r.data.status,
          router: this.$route.query.router,
          direction: this.details.to,
          directionNo: this.direction,
          stopInfo: {
            stopName: item.stop_name,
            stopId: item.stop_id,

          },
          left: {
            time: r.data.time,
            distance: r.data.distance,
            stopInterval: r.data.stop_interval
          }
        }
        this.$loading.close()
      })
    }
  },
  watch: {
  }
}
</script>
<style type="text/css" scoped>
  .page-container {
    background: #fff;
  }
  .page-body {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: .5rem;
    overflow: auto;
  }
  .direction {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: .6rem;
    padding: 0 .15rem;
    border-bottom: 1px solid #ccc;
  }
  .direction .left {

  }
  .direction .exchange {
    width: .35rem;
    height: .35rem;
    background: url(icons8-synchronize-64.png);
    background-size: cover;
  }
  .detail-list {
    padding: 0 .15rem;
  }
  .detail-list .item {
    line-height: 2;
  }
</style>