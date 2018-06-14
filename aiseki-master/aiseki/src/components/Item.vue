<template>
  <div id="main" class="item">
<div class="wrapper">
    <p class="bread-crumb">
        <router-link :to="{ path: '/' }">TOP</router-link> / 
        <router-link :to="{ path: '/list',query:{area_parent:area_parent,area_child:''} }">{{area_parent?area_parent:'未選択'}}</router-link> / 
        <router-link :to="{ path: '/list',query:{area_parent:area_parent,area_child:area_child} }" v-if="area_child">{{area_child}}</router-link>
        <span v-if="!area_child">未選択</span>
        </p>
    <p class="name">{{item.name}}</p>
    <dl>
        <dt>住所</dt>
        <dd>{{item.address}}</dd>
        <p class="googlemap"><a :href="item.map_url" target="_blank">Google map</a></p>
        <dt>営業時間</dt>
        <dd>{{item.open_time}}</dd>
        <dt>アクセス</dt>
        <dd>熊本市電 花畑町駅 徒歩3分 </dd>
        <dt>TEL</dt>
        <dd><a :href="'tel:'+ item.tel">{{item.tel}}</a></dd>
        <dt>公式HP</dt>
        <dd><a :href="item.site" target="_blank">{{item.site}}</a></dd>
    </dl>
    <div class="number clearfix" v-if="'men' in this.visitor">
        <div class="men float-left">
            <p><img src="https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/pict_men.png" width="auto" height="24">{{visitor.men}}<small>{{visitor.type}}</small></p>
        </div>
        <div class="women float-right">
            <p><img src="https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/pict_women.png" width="auto" height="24">{{visitor.women}}<small>{{visitor.type}}</small></p>
        </div>
    </div>
    <div class="comment">
        <p class="head">コメント</p>
        <div v-for="comment in this.comments" v-bind:class="comment.gender == 0 ? 'men':'women'" class="clearfix">
            <div class="avatar"><img v-bind:src="comment.gender == 0 ? 'https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/pict_men.png'
                :'https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/pict_women.png'">
                <p class="name">{{comment.user_name}}</p>
                <p class="date">{{ new Date(comment.created * 1000).toLocaleString()}}</p>
            </div>
            <div class="text">
                <p>{{comment.comment}}</p>
            </div>
        </div>

        <div class="write">
            <p class="head">コメントする</p>
            <textarea class="textbox" v-model="post_comment"></textarea>
            <div class="gender">
                <div class="custom-control custom-control-inline">
                    <input type="radio" id="customRadioInline1" name="gender" value="0" v-model="post_gender">
                    <label for="customRadioInline1">男性</label>
                </div>
                <div class="custom-control custom-control-inline">
                    <input type="radio" id="customRadioInline2" name="gender" value="1" v-model="post_gender">
                    <label for="customRadioInline2">女性</label>
                </div>
            </div>
            <div class="write"><a v-on:click="put_comment()">投稿</a></div>
        </div>
    </div>
    </div>
</div>
</template>

<style>
.write label{
    padding-left: .5em;
}
input[type='radio']{
    margin-top: 0.3px;
}
</style>


<script>
import api from "../api";

export default {
  name: 'List',
  data () {
    return {
      item:{},
      comments:[],
      id:this.$route.query.id,
      area_parent:this.$route.query.area_parent,
      area_child:this.$route.query.area_child,
      post_comment:'',
      post_gender:0,
      visitor:{}
    }
  },
  created() {
    // Json取得
    api.get_static_json('aiseki.json', 'aiseki');
    api.get_static_json('visitor.json', 'visitor');
    api.get('comment/'+this.id, {}, 'aiseki_comments');
    // Json取得後に呼び出される
    api.$on('GET_STATIC_JSON_COMPLETE', () => {
      let list = api.get_data('aiseki');
      list.forEach(item => {
          if(item.id == this.id)this.item = item;
      });
      list = api.get_data('visitor');
      list.forEach(item => {
          if(item.aiseki_id == this.id)this.visitor = item;
      });
    });
    api.$on('GET_COMPLETE', () => {
      let comments = api.get_data('aiseki_comments');
      if(comments.length > 0)this.comments = comments;
    });
    api.$on('POST_COMPLETE', () => {
      const now = new Date();
      this.comments.unshift({
        comment:this.post_comment,
        aiseki_id:this.id,
        user_name:this.post_gender==0?'太郎':'花子',
        gender:this.post_gender,
        created: Math.floor( now.getTime() / 1000 )
      });
      this.post_comment = '';
    });
  },
  methods:{
      put_comment(){
          if(this.post_comment == '' || (this.post_gender !=0 && this.post_gender !=1)){
              return;
          }
          let request = {
              comment:this.post_comment,
              aiseki_id:this.id,
              user_name:this.post_gender==0?'太郎':'花子',
              gender:this.post_gender
          }
          api.post('comment', request, '');
      }
  }
}
</script>