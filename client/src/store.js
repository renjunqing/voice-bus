import Vue from 'vue'

export default new Vue({
	data() {
		return {
			watchList: []
		}
	},
  created() {
    this.watchList = JSON.parse(window.localStorage.watchList || '[]')
  },
	methods: {
		watchNew(newOne) {
      if (this.watchList.find(v => v.router === newOne.router && v.stopInfo.stopId === newOne.stopInfo.stopId && v.direction === newOne.direction)) {
        window.alert('已关注本站点，无需重复关注')
        return
      }
      this.watchList.push(newOne)
    },
    cancelWatch(newOne) {
      this.watchList = this.watchList.filter(v => !(v.router === newOne.router && v.stopInfo.stopId === newOne.stopInfo.stopId && v.direction === newOne.direction))
    },
    refreshWatchList(watchList) {
      this.watchList = watchList.filter(v => true)
    },
    getWatchList() {
      return this.watchList
    }
	},
  watch: {
    watchList() {
      window.localStorage.watchList = JSON.stringify(this.watchList)
    }
  }
})