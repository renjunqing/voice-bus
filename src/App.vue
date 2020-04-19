<template>
  <div id="app">
  	<transition :name="transitionName">
  	  <router-view class="router-view"></router-view>
  	</transition>
  </div>
</template>

<script>
import {request} from './util/index.js'
export default {
  name: 'App',
  data() {
    return {
      transitionName: 'slide-left',
      routeHistory: [],
      version: '1.0'
    }
  },
  created() {
    var that = this
    this.routeHistory.push(this.$route)
    var routeHistory = this.routeHistory
    window.document.addEventListener('plusready', function(){
      window.plus.device.setWakelock(true);
      plus.key.addEventListener('backbutton', () => {
        try {
          window.history.go(-1)
          if (routeHistory.length <= 1) {
            var c = window.confirm('确定退出应用吗？')
            c && plus.runtime.quit()
          }
        } catch(e) {
          window.alert('抱歉，运行错误，即将退出应用！')
          plus.runtime.quit()
        }
      })
      that.checkUpdate()
    })
  },
  watch: {
	  '$route'(to, from) {
      var lastRoute = this.routeHistory[this.routeHistory.length - 2]
      if (lastRoute && lastRoute.path === to.path) {
        this.transitionName = 'slide-right'
        this.routeHistory.pop()
      } else {
        this.transitionName = 'slide-left'
        this.routeHistory.push(to)
      }	    
	  }
	},
  methods: {
    checkUpdate() {
      request('bus/check_update',{}, {
        version: this.version,
        platform: 'android'
      }).then(r => {
        if (r.data.version && window.confirm('检测到新版本：' + r.data.version)) {
          window.open(r.data.link)
        }
      })
    },
  }
}
</script>
<style>
.router-view {
  transition: left .3s ease-out;
  position: relative;
  padding-top: .5rem;
  box-sizing: border-box;
}

.slide-left-enter {
  left: 3.75rem;
}
.slide-left-enter-active {
  top: -100%;
}
.slide-left-enter-to {
  left: 0;
}
.slide-right-enter-active {
  top: -100%;
  z-index: 1;
}
.slide-right-leave {
  left: 0;
}
.slide-right-leave-active {
  z-index: 2;
}
.slide-right-leave-to {
  left: 3.75rem;
}
</style>
