<template>
	<div class="page-container">
    <pageHeader title="搜索公交线路"></pageHeader>
    <input v-model="searchStr" type="text" name="" placeholder="请输入公交线路名称">
    <div class="search-result">
      <router-link v-for="item in searchResults" :to="'/routerDetail?router=' + item">
        <div class="item">{{item}}</div>
      </router-link>
    </div>
  </div>
</template>
<script type="text/javascript">
import {request} from '../util/index.js'
import pageHeader from '../components/header.vue'
export default {
  data () {
    return {
      searchStr: null,
      searchResults: []
    }
  },
  components: {
    pageHeader
  },
  created() {
  },
  methods: {
    goSearch() {
      this.$router.push({
        path: 'search'
      })
    }
  },
  watch: {
    searchStr() {
      if (this.searchStr.length >= 2) {
        request('bus/<router_name_str>/search', {
          router_name_str: this.searchStr
        }).then(result => {
          this.searchResults = result.data
        })
      }
    }
  }
}
</script>
<style type="text/css" scoped>
  .page-container {
    background: #fff;
  }
  input {
    line-height: .5rem;
    border: none;
    border-bottom: solid 1px #ccc;
    outline: none;
    background: transparent;
    font-size: .2rem;
    display: block;
    margin: 0 .2rem;
  }
  .search-result {
    display: flex;
    flex-wrap: wrap;
    padding: .2rem;
  }
  .search-result .item {
    background: #1abc9c;
    color: #fff;
    border-radius: 3px;
    line-height: .3rem;
    padding: 0 .1rem;
    margin: 0 .1rem .1rem 0;
    text-decoration: none;
  }
</style>