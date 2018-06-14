import Vue from 'Vue';

// Ajax通信ライブラリ
import axios from 'axios';
const STATIC_JSON_URL_BASE = 'https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/assets/json/';
const URL_BASE = 'https://7c863hmsth.execute-api.ap-northeast-1.amazonaws.com/aiseki/';

export default new Vue({
    data: {
        // Jsonデータ格納用
        area: [],
        aiseki:[],
        aiseki_comments:[],
        visitor:[]
    },
    methods: {
        // Ajax通信でJsonを取得し、特定のプロパティに格納する
        // 取得したら GET_AJAX_COMPLETE で通知する
        get_static_json(url, name) {
          return axios.get(STATIC_JSON_URL_BASE + url)
          .then((res) => {
            Vue.set(this, name, res.data);
            this.$emit('GET_STATIC_JSON_COMPLETE');
          });
        },
        get(url, option, name){
          return axios.get(URL_BASE + url, option)
          .then((res) => {
              Vue.set(this, name, res.data);
              this.$emit('GET_COMPLETE');
            });
        },
        post(url, option, name) {
          return axios.post(URL_BASE + url, option)
            .then((res) => {
              Vue.set(this, name, res.data);
              this.$emit('POST_COMPLETE');
            });
      },
        // プロパティ名を指定してデータを取得
        get_data(name) {
          return this.$data[name];
        }
    }
})