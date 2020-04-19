import axios from 'axios'
export function request(url, params, query = {}) {
  if (params) {
    Object.keys(params).forEach(p => {
      url = url.replace(new RegExp('<' + p + '>', 'ig'), params[p])
    })
    url = url.replace(/\<|\>/ig, '')
  }
  query.test = true
	return axios.get('http://voice_bus.puzhibaike.com/api/' + url, {params: query})
}