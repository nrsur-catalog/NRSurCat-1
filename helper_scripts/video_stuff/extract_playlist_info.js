var thumbnails = document.getElementsByClassName('yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded');
var dataList = "title,id,thumbnail\n";
for(i = 0;i<els.length;i++){
    var el = els[i];
    var t = thumbnails[i];
    var curId = el.href.split('?v=')[1].split('&list')[0];
    dataList += (el.title + "," + curId + "," + t.src + "\n");
}
console.log(dataList);