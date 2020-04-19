<template>
	<div class="page-container">
    <pageHeader title="使用帮助"></pageHeader>
    <div>
      <ul>
        <li>1. 初次使用时，请先添加要关注的公交线路及站点，添加完成之后回到首页的关注列表。</li>
        <li>2. 在首页的关注列表中，点亮某个站点小闹钟，即可实时监控公交到站时间，并语音播报。</li>
        <li>3. 最多可同时监控两个站点，监控频率为每分钟一次。</li>
        <li>4. 有任何使用上的问题可联系<a href="mailto: voice_bus@youjihua.net">voice_bus@youjihua.net</a>反馈。</li>
        <li class="red">5. 实时监控需要常驻后台运行，需用户根据自己的手机系统设置，保证应用后台进程不被（系统或第三方清理程序）清理，使用完毕后手动退出。</li>
      </ul>
    </div>
  </div>
</template>
<script type="text/javascript">
import pageHeader from '../components/header.vue'
export default {
  data () {
    return {
    }
  },
  components: {
    pageHeader
  },
  created() {
  },
}
</script>
<style type="text/css" scoped>
  .page-container {
    background: #fff;
  }
  li {
    font-size: .14rem;
    color: #666;
    padding: 0 .1rem;
    margin: .08rem 0;
  }
  .red {
    color: red;
  }
</style>