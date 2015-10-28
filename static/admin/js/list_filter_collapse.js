/*
Pluggable javascript for Django admin.
Taken from Github gist https://gist.github.com/jjdelc/985283 by jjdelc
 */

;(function($){
ListFilterCollapsePrototype = {
    bindToggle: function(){
        var that = this;
        this.$filterEl.click(function(){
            that.$filterList.slideToggle();
        });
    },
    init: function(filterEl) {
        this.$filterEl = $(filterEl).css('cursor', 'pointer');
        this.$filterList = this.$filterEl.next('ul').hide();
        this.bindToggle();
    }
}
function ListFilterCollapse(filterEl) {
    this.init(filterEl);
}
ListFilterCollapse.prototype = ListFilterCollapsePrototype;

$(document).ready(function(){
    $('#changelist-filter').children('h3').each(function(){
        var collapser = new ListFilterCollapse(this);
    });
});
})(django.jQuery);