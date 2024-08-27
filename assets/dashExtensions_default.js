window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(e, ctx) {
            ctx.map.flyTo([-120, 120], 1);
        },
        function1: function(e, ctx) {
            console.log(`Clicked coordinates: ${e.latlng}, map center: ${ctx.map.getCenter()}`);
        }
    }
});