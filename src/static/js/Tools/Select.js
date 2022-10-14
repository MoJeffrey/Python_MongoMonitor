/**
 * 下拉項
 * 依賴 Jquery 和 Layui
 * 主要用於異步獲取資料和渲染下拉項
 */

class Select{
    // 下拉項元素ID
    ElementId = null;
    // Layui 的Form 用於渲染異步結果
    form = null;
    // Post 數據
    PostData = null;

    constructor(ElementId, form, PostData={}) {
        this.ElementId = ElementId;
        this.form = form;
        this.PostData = PostData;
    }

    /***
     * 請求實例化
     */
    AjaxInstantiate(URL){
        let Data = null;
        let Self = this;
        $.ajax({
            type: 'post',
            url: URL,
            data: this.PostData,
            async: false,
            success: function (data) {
                if (data.code === 200) {
                    Data = data['data'];
                    Self.DataInstantiate(Data);
                } else {
                    layer.alert(data.msg, {icon: 2});
                }
            }
        });
        return Data
    }

    /**
     * 直接數據實例化
     * @param Data
     * @constructor
     */
    DataInstantiate(Data){
        let Select = document.getElementById(this.ElementId);
        for(let Num in Data) {
            if(Data.hasOwnProperty(Num)){
                let option = document.createElement("option");
                option.setAttribute("value", Data[Num]['id']);
                option.innerText = Data[Num]['Name'];
                Select.appendChild(option);
            }
        }
        form.render("select");
    }

    /**
     * 直接渲染和請求數據
     * @param ElementId
     * @param form
     * @param URL
     * @param PostData 請求數據
     * @returns 請求到的List
     */
    static Ajax(ElementId, form, URL, PostData=[]){
        return new Select(ElementId, form, PostData).AjaxInstantiate(URL);
    }

    /**
     * 直接用數據渲染下拉項
     * @param ElementId
     * @param form
     * @param Data
     */
    static Data(ElementId, form, Data){
        new Select(ElementId, form).DataInstantiate(Data);
    }
}