/**
 * 提示
 * 依賴 Layui
 * 多數會用於Ajax
 */

class Prompt{
    /**
     * 跳出Loading 提示
     */
    static Loading(msg) {
        return layer.msg(msg, {icon: 16, shade: 0.3, time: 0});
    }

    /**
     * 跳出錯誤
     */
    static Error(Msg){
        return layer.alert(Msg, {icon: 2});
    }

}