var basePath = 'http://106.13.87.73:8999';
App({
  //自定义全局属性
  curid: "CN101010100",
  version: "1.0",
  userInfo: null,
  data: {
    basePath: basePath,
  },
  globalData: {
    userInfo: null,
    scence: 0,
    GDBTestShow: 0,
  },
  //系统事件
  onLaunch: function () {//小程序初始化事件
    //console.log("launch");
    var that=this;
    //调用API从本地缓存中获取数据
    that.curid = wx.getStorageSync('curid') || that.curid;//API：获取本地缓存，若不存在设置为全局属性
    that.setlocal('curid', that.curid);//调用全局方法
    wx.setBackgroundColor({
      backgroundColorTop: '#b4189d', // 顶部窗口的背景色
      backgroundColorBottom: '#f7f7f9', // 底部窗口的背景色
    })
  },

  //自定义全局方法
  setlocal:function(id,val){  
    wx.setStorageSync(id, val);//API：设置本地缓存
  },


  // getuserinfo 暂时我是不需要,不需要
  getUserInfo: function (cb) {
    console.log("getUserInfo", this.globalData.userInfo);
    var that = this
    if (this.globalData.userInfo) {
      typeof cb == "function" && cb(this.globalData.userInfo)
    } else {
      console.log("调用登陆接口");
      
      wx.login({
        success: function (res) {
          if(res.code){
            console.log("code:",res.code);
          }
          wx.getUserInfo({
            success: function (res) {
              console.log(res);
              that.globalData.userInfo = res.userInfo
              typeof cb == "function" && cb(that.globalData.userInfo)
            },
            fail: function (res) {
              console.log(res);
            }
          })
        }
      })
    }
  },




  //请求头封装
  getRequestHeader:function(){
    return {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': this.getCache( "token" )
    }
  },
  getCache:function( key ){
    var value = undefined;
    try {
        value = wx.getStorageSync( key );
    } catch (e) {
    }
    return value;
  },
  setCache:function(key,value){
      wx.setStorage({
          key:key,
          data:value
      });
  },
  alert:function( params ){
    var title = params.hasOwnProperty('title')?params['title']:'答题系统提示您';
    var content = params.hasOwnProperty('content')?params['content']:'';
    wx.showModal({
        title: title,
        content: content,
        showCancel:false,
        success: function(res) {
            if (res.confirm) {//用户点击确定
                if( params.hasOwnProperty('cb_confirm') && typeof( params.cb_confirm ) == "function" ){
                    params.cb_confirm();
                }
            }else{
                if( params.hasOwnProperty('cb_cancel') && typeof( params.cb_cancel ) == "function" ){
                    params.cb_cancel();
                }
            }
        }
    })
},






  // 显然觉得这些方法写在这块不合适，先这么着吧。
  setVip9Status:function(phone,productType){
    wx.request({
      url: basePath+'/TiKu/getIsVip9.do',
      data: {
        phone: phone,
        productType:productType
      },
      success:function(data){
        wx.setStorageSync("isVip9", data.data);
      }
    })
  },
  // 获取用户信息
  setUserMessage:function(username){
    wx.request({
      url: basePath + '/jcuser/getJcUserByUsername.do',
      data: {
        username: username,
      },
      success: function (data) {
        wx.setStorageSync("jcuser", data.data);
      }
    })
  },
  // 获取用户笔记错题，笔记，收藏信息
  setThreeData:function(username,productType){
    wx.request({
      url: basePath + '/TiKu/getThreeDataList.do',
      data: {
        username: username,
        productType: productType
      },
      success:function(data){
        wx.setStorageSync("threeData", data.data);
      }
    })
  },
  onShow: function (options) {
    console.log("场景值" + options.scene)
  },
  onHide: function () {
    console.log("App生命周期函数——onHide函数");
  },
  onError: function (msg) {
    console.log("App生命周期函数——onError函数");
  },
  
  set3Method(username, productType){
    //1 vip9
    wx.request({
      url: basePath + '/TiKu/getIsVip9.do',
      data: {
        phone: username,
        productType: productType
      },
      success: function (data) {
        wx.setStorageSync("isVip9", data.data);
      }
    })
    //2 jcuser
    wx.request({
      url: basePath + '/jcuser/getJcUserByUsername.do',
      data: {
        username: username,
      },
      success: function (data) {
        wx.setStorageSync("jcuser", data.data);
      }
    })
    //3
    wx.request({
      url: basePath + '/TiKu/getThreeDataList.do',
      data: {
        username: username,
        productType: productType
      },
      success: function (data) {
        wx.setStorageSync("threeData", data.data);
      }
    })
  }
})
