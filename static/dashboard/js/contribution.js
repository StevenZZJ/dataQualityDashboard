/**
 * Jquery to render a contribution graph like github
 * @Author  LIUDu
 *
 */


// Format string
if (!String.prototype.formatString) {
    String.prototype.formatString = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}

(function ($) {


    $.fn.github_graph = function (options) {

        // Get the total number of files
        var getTotalNum = function (data_t) {
            var num = data_t.id.length
            return num
        }

        // Get the color of each file
        var getColor = function (countErr) {
            if (countErr >= 150) {
                return settings.colors[settings.colors.length - 5];
            }
            if (countErr >= 100) {
                return settings.colors[settings.colors.length - 4];
            }
            if (countErr >= 80) {
                return settings.colors[settings.colors.length - 3];
            }
            if (countErr >= 30) {
                return settings.colors[settings.colors.length - 2];
            } else {
                return settings.colors[settings.colors.length - 1]
            }
        }

        var start =
            function () {
                var countNum = getTotalNum(settings.data);
                var color = getColor(settings.data.id[0].Err);
                // $('body').append('<div>' + '<h1>Total Number :' + countNum + '</h1> </div>');
                settings.colors_length = settings.colors.length;

                var wrap_chart = _this;


                var step = 13;
                var loop_html = "";
                var numc = 0;
                for (var i = 0; i < countNum / 5; i++) {
                    var g_x = i * step;
                    var item_html = '<g transform="translate(' + g_x.toString() + ',0)">';

                    for (var j = 0; j < 5; j++) {
                        var y = j * step;
                        if (numc >= countNum) {
                            break
                        } else {
                            var color = getColor(settings.data.id[numc].Err);
                            var urlOfFile = settings.data.id[numc].url;
                            var errCount = settings.data.id[numc].Err;
                            var datasetName = settings.data.id[numc].name;
                            var dataDupli = settings.data.id[numc].dupliRate;
                            var datasetComplet = settings.data.id[numc].completeness;
                            item_html += '<a href="' + urlOfFile + '"><rect class="day" width=11 height="11" y="' + y + '" fill="' + color + '" data-count="' + errCount + '" data-name="' + datasetName + '"data-dup="' + dataDupli + '"   data-complet="' + datasetComplet + '" /></a>';
                            numc++;
                        }
                    }

                    item_html += "</g>";

                    loop_html += item_html;
                }


                var wire_html =
                    '<svg width="721" height="110" viewBox="0 0 721 110"  class="js-calendar-graph-svg">' +
                    '<g transform="translate(20, 20)">' +
                    loop_html +
                    '</g>' +
                    '</svg>';

                wrap_chart.html(wire_html);

                _this.find('rect').on("mouseenter", mouseEnter);
                _this.find('rect').on("mouseleave", mouseLeave);
                appendTooltip();
            }

        //Mare sure off previous event
        /*$(document).off('mouseenter', _this.find('rect'), mouseEnter );
        $(document).off('mouseleave', _this.find('rect'), mouseLeave );
        $(document).on('mouseenter', _this.find('rect'), mouseEnter );
        $(document).on('mouseleave', _this.find('rect'), mouseLeave );
*/


        var mouseLeave = function (evt) {
            $('.svg-tip').hide();
        }

        //handle event mouseenter when enter into rect element
        var mouseEnter = function (evt) {

            var target_offset = $(evt.target).offset();
            var targetName = $(evt.target).attr('data-name');
            var targetDupRate = $(evt.target).attr('data-dup');
            var targetCompleteness = $(evt.target).attr('data-complet');
            var count = $(evt.target).attr('data-count');


            var text = "<p>Dataset name:{0} <br/> DuplicateRate:{1} <br/> Completeness:{2} <br/> ErrorCount:{3}</p>".formatString(targetName, targetDupRate, targetCompleteness, count);

            var svg_tip = $('.svg-tip').show();
            svg_tip.html(text);
            var svg_width = Math.round(svg_tip.width() / 2 + 5);
            var svg_height = svg_tip.height() * 2 + 10;

            svg_tip.css({top: target_offset.top - svg_height - 5});
            svg_tip.css({left: target_offset.left - svg_width});
        }
        //Append tooltip to display when mouse enter the rect element
        //Default is display:none
        var appendTooltip = function () {
            if ($('.svg-tip').length == 0) {
                $('body').append('<div class="svg-tip svg-tip-one-line" style="display:none">   </div>');
            }
        }


        var settings = $.extend({
            //Default init settings.colors, user can override
            colors: ['#eeeeee', '#d6e685', '#8cc665', '#44a340', '#44a340'],
            start: null,
            data: null,
        }, options);

        var _this = $(this);

        start();

    };

}(jQuery));