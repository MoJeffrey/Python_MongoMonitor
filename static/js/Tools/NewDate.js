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
        let ms = date.getMilliseconds();

        date = date.toJSON();
        date = date + " : " + ms;
        if(OnlyDate){
            date = date.split('T')[0];
        }

        return date
    }

}