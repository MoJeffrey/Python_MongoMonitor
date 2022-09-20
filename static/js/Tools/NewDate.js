/**
 * 對時間的處理
 */

class NewDate{

    /**
     * 獲取日期 e.g 20211121
     * @param time
     * @param OnlyDate
     * @returns {Date}
     * @constructor
     */
    static GetDate(time = +new Date(), OnlyDate=true) {
        let date = new Date(time + 8 * 3600 * 1000);

        date = date.toJSON().substr(0, 19);

        if(OnlyDate){
            date = date.split('T')[0];
        }

        return date
    }

}