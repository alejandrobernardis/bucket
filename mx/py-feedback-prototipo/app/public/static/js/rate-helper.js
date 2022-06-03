$(function(){
    $('.js-rate-helper').popover({
        html: true,
        trigger: 'hover',
        container: 'body',
        delay: 10,
        title: 'Calificaciones:',
        content: function(){
            return '<ul class="rate-helper">'
                + '<li><img src="/static/img/icons/color/1.png" alt="Muy Mala"/> Muy Mala</li>'
                + '<li><img src="/static/img/icons/color/2.png" alt="Mala"/> Mala</li>'
                + '<li><img src="/static/img/icons/color/3.png" alt="Regular"/> Regular</li>'
                + '<li><img src="/static/img/icons/color/4.png" alt="Bien"/> Bien</li>'
                + '<li><img src="/static/img/icons/color/5.png" alt="Muy Bien"/> Muy Bien</li>'
                + '</ul>';
        }
    });
});