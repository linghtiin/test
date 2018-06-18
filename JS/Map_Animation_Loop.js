//=============================================================================
// Map_Animation_Loop.js
//=============================================================================
/*:
 *@plugindesc 在地图上为事件或玩家增加一个循环播放的动画，与其他动画不冲突
 *@author CHEESE_JEROME
 *
 *@help
 *18/5/14
 *
 *使用方法：
 *
 *在事件页中添加事件指令：「注释…」，
 *然后输入「<animationLoop:5>」
 *（需要为独立的一个注释指令！）
 *这样，这个事件就会循环播放5号动画，直到事件页更改为止。
 *  
 * 注：这个循环动画是完全独立的，可以与其他动画同时播放。
 * 
 * 其他使用方法：
 * 
 * 1）更改玩家的循环动画
 * 设置一个事件脚本：「this.character(-1).setAnimationLoop(15)」
 * 执行后，玩家身上将会循环播放15号动画，这个效果会一直持续。
 * 停止方法：「this.character(-1).setAnimationLoop(0)」
 * 
 * 2）暂时更改事件的循环动画
 * 在事件中添加脚本「this.character(this._eventId).setAnimationLoop(15)」，
 * 执行后，可以将循环动画的编号暂时改为15号（改为0号时，将会停止循环动画的播放）。
 * 这个功能是暂时的：每当地图刷新或事件刷新后，
 * 循环动画的编号又会返回最初注释内设定的那个。
 */
var Map_Animation_Loop = Map_Animation_Loop || {};
//利用事件编辑器的注释功能，为事件页增加新属性
Map_Animation_Loop._Game_Event_setupPageSettings = Game_Event.prototype.setupPageSettings;
Game_Event.prototype.setupPageSettings = function() {
    //初始化
    this._animationLoop = 0 ;
    //读取事件页中的注释
    Map_Animation_Loop._Game_Event_setupPageSettings.call(this);
    //遍历事件页
    for (var i = 0; i < this.list().length; i++) {
        //寻找「注释」事件
        if (this.list()[i].code === 108){
            //循环动画ID（当这个事件需要循环播放动画时指定）
            if(this.list()[i].parameters[0].match(/<(?:animationLoop):(\d+)>/)){
                this._animationLoop = Number(RegExp.$1);
            }
        }
    }
};
/**循环动画id*/
Game_CharacterBase.prototype.animationLoop = function() {
    //返回 循环动画id
    return this._animationLoop;
};
/**设置循环动画id（于事件编辑器内使用）*/
Game_CharacterBase.prototype.setAnimationLoop = function(animationLoop) {
    //设置 循环动画id
    this._animationLoop = animationLoop
};
/**更新动画 */
Map_Animation_Loop._Sprite_Character_updateAnimation = Sprite_Character.prototype.updateAnimation;
Sprite_Character.prototype.updateAnimation = function (){
    /**安装循环动画 */
    this.setupAnimationLoop();
    Map_Animation_Loop._Sprite_Character_updateAnimation.call(this);
}
/**安装循环动画 */
Sprite_Base.prototype.setupAnimationLoop = function() {
    //检测循环动画编号是否同步，若不同步则执行
    if (this._animationLoop != this._character.animationLoop()){
        //若已存在循环动画精灵，移除循环动画精灵
        if (this._animationLoopSprite) this._animationLoopSprite.remove();
        //同步循环动画编号
        this._animationLoop = this._character.animationLoop();
        //若循环编号为真
        if (this._animationLoop){
            //循环动画精灵 = 新 精灵动画()
            this._animationLoopSprite = new Sprite_Animation();
            //循环动画精灵 安装(效果 ,动画, 镜像, 延迟)
            this._animationLoopSprite.setup(this._effectTarget, $dataAnimations[this._animationLoop],  false, 0);
            //父类 添加子项(循环动画精灵) 
            this.parent.addChild(this._animationLoopSprite);
        }
    }
};
/**更新 */
Map_Animation_Loop._Sprite_Base_update = Sprite_Base.prototype.update;
Sprite_Base.prototype.update = function() {
    /**更新循环动画 */
    Map_Animation_Loop._Sprite_Base_update.call(this);
    this.updateAnimationLoop();
};
/**更新循环动画 */
Sprite_Base.prototype.updateAnimationLoop = function(){
    //如果存在循环动画精灵 && 持续时间已经结束
    if (this._animationLoopSprite && !this._animationLoopSprite.isPlaying()) {
        //重置持续时间
        this._animationLoopSprite.setupDuration()
    }
};