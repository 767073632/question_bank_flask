// pages/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    "itemIcon":[
      "../../images/add.png",
      "../../images/add.png",
      "../../images/add.png",
      "../../images/add.png",
      ""
    ],
    "innerTitleStyle":[
      "display:none",
      "display:none",
      "display:none",
      "display:none",
      "",
    ],
    "pulldownIcon":"../../images/down.png",
    "checkStyle":"display:none",
    "progressIndex":"",
    "percent": 50,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  drawProgressbg: function(){
    // 使用 wx.createContext 获取绘图上下文 context
    var ctx = wx.createCanvasContext('canvasProgressbg',this)
    ctx.setLineWidth(4);// 设置圆环的宽度
    ctx.setStrokeStyle('#c441a9'); // 设置圆环的颜色
    ctx.setLineCap('round') // 设置圆环端点的形状
    ctx.beginPath();//开始一个新的路径
    ctx.arc(50, 50, 40, 0, 2 * Math.PI, false);
    //设置一个原点(110,110)，半径为100的圆的路径到当前路径
    ctx.stroke();//对当前路径进行描边
    ctx.draw();
  },

  drawCircle: function (step){  
    var context = wx.createCanvasContext('canvasProgress',this);
      // 设置渐变
      var gradient = context.createLinearGradient(200, 100, 100, 200);
      gradient.addColorStop("0", "#2661DD");
      gradient.addColorStop("0.5", "#40ED94");
      gradient.addColorStop("1.0", "#5956CC");
      
      context.setLineWidth(4);
      context.setStrokeStyle(gradient);
      context.setLineCap('round')
      context.beginPath(); 
      // 参数step 为绘制的圆环周长，从0到2为一周 。 -Math.PI / 2 将起始角设在12点钟位置 ，结束角 通过改变 step 的值确定
      context.arc(50, 50, 40, -Math.PI / 2, step * Math.PI - Math.PI / 2, false);
      context.stroke(); 
      context.draw() 
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    this.drawProgressbg();
    this.drawCircle(this.data.percent * 2 / 100);
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
    
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  //点击练习
  exercise:function(){
    wx.navigateTo({
      url: '../exercise/exercise',
    })
  },

  //随机练习
  randomPractice:function(){
    wx.navigateTo({
      url: '../exercise/exercise',
    })
  },

   //错题集
   failQuestion:function(){
    wx.navigateTo({
      url: '../history/index',
    })
  },

  //收藏
  collection:function(){
    wx.navigateTo({
      url: '../history/index',
    })
  },

  //笔记
  notes:function(){
    wx.navigateTo({
      url: '../history/index',
    })
  },

  //练习历史
  practiseHistory:function(){
    wx.navigateTo({
      url: '../history/index',
    })
  },

  //题库设置
  questionSetting:function(){
    wx.navigateTo({
      url: '../history/index',
    })
  },

  //展开
  extend:function(e){
    var num = e.target.dataset.number;
    var image = this.data.itemIcon[num];
    if (image == '../../images/add.png'){
      this.data.itemIcon[num] = '../../images/sub.png'
      this.data.innerTitleStyle[num] = 'display:block';
    } else if (image == '../../images/sub.png'){
      this.data.itemIcon[num] = '../../images/add.png'
      this.data.innerTitleStyle[num] = 'display:none';
    }
    var newItemIcon = this.data.itemIcon;
    this.setData({
      "itemIcon":newItemIcon,
      "innerTitleStyle":this.data.innerTitleStyle
    })
  },

  //下拉框
  pullDown:function(e){
    this.setData({
      "pulldownIcon":'../../images/open_right.png',
      "checkStyle":'',
      "progressIndex":"display:none"
    })
  },

  stopScroll:function(e){},

  //弹出框消失
  checkNone:function(e){
    this.setData({
      "pulldownIcon":'../../images/down.png',
      "checkStyle":'display:none',
      "progressIndex":""
    })
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})