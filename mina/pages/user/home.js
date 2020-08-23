// pages/index.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    //判断小程序的API，回调，参数，组件等是否在当前版本可用。
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    isHide: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.setBackgroundColor({
      backgroundColorTop: '#b4189d', // 顶部窗口的背景色
      backgroundColorBottom: '#f7f7f9', // 底部窗口的背景色
    });
    // 查看是否授权
    this.checkLogin();
  },
  //检查是否登录
  checkLogin:function(){
    var that = this;
     wx.login({
         success:function( res ){
            if( !res.code ){
                app.alert( { 'content':'登录失败，请再次点击~~' } );
            };
             wx.request({
                url:'http://127.0.0.1:9000/api/member/check-reg',
                header:app.getRequestHeader(),
                method:'POST',
                data:{ code:res.code },
                success:function( res ){
                    if( res.data.code != 200 ){
                        that.setData({
                          isHide:true
                        });
                        return;
                    }
                    
                    app.setCache( "token",res.data.data.token );
                    //that.goToIndex();
                },
                fail:function(res){
                  console.log(res)
                }
            });
         }
     })
      
  },
  //这边是用户点击的登录按钮
  bindGetUserInfo: function(e) {
    if (e.detail.userInfo) {
        var that = this;
        wx.getUserInfo({
          success: function(res) {
              wx.login({
                  success: res => {
                      var userInfo = e.detail.userInfo;
                      if( !res.code ){
                        app.alert( { 'content':'登录失败，请再次点击~~' } );
                        return;
                      }
                      userInfo['code'] = res.code;
                      that.setData({
                        userInfo:userInfo
                      })
                      
                      wx.request({
                          url: 'http://127.0.0.1:9000/api/member/login',//请求url
                          data:userInfo,
                          header:app.getRequestHeader(),
                          method:'POST',
                          success: res => {
                            if( res.data.code != 200 ){
                              app.alert( { 'content':res.data.msg } );
                              return;
                             }
                           app.setCache( "token",res.data.data.token );
                           that.setData({
                            isHide:false
                          });
                           wx.switchTab({
                            url: '/pages/index/index',
                            });
                          }
                      });
                  }
              });
          }
      });
        this.setData({
          userInfo:e.detail.userInfo,
          // isHide: false//登录成功把这个注释去掉
        })
    } else {
        //用户按了拒绝按钮
        wx.showModal({
            title: '警告',
            content: '您点击了拒绝授权，将无法进入小程序，请授权之后再进入!!!',
            showCancel: false,
            confirmText: '返回授权',
            success: function(res) {
                // 用户没有授权成功，不需要改变 isHide 的值
                if (res.confirm) {
                    console.log('用户点击了“返回授权”');
                }
            }
        });
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    wx.setBackgroundColor({
      backgroundColorTop: '#b4189d', // 顶部窗口的背景色
      backgroundColorBottom: '#f7f7f9', // 底部窗口的背景色
    })
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})