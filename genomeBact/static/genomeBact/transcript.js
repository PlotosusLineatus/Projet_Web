
var width = 1200;
var height = 200;
var s_size = 10000;
var width_svg = 1200-60;
var seqlen = length;
let background = "#FBF5F3"
let cds_color = "#8DAA9D";
let over_color = "#45425A";


let list = list_cds;

var svg= d3.select("#svg_genomic_view").append("svg")
              .attr("width", width)
              .attr("height", height)
              .attr("id", "svg")
              .style("background", background)
              ;

genomic_view(s_size);
function genomic_view(s_size){
  
  var svg_rect = svg.append("g").attr("id", "rectangle");
  rectangle(0,30, svg_rect);
  rectangle(width-30,width, svg_rect);

  axis(1, s_size);
  //fleche();
  //d3.select("[id=fleche]")
  //.attr("transform",'translate(30,0)');
  

  var svg_cds = svg.append("g").attr("id", "cds")
  .style('fill', cds_color);


  //let list_cds = {"cds_1" :cds_1, "cds_2" :cds_2};
  let list_coord_cds = {};
  for(i in list){    
    list_coord_cds["cds_"+list[i].id] = cds(list[i], 1, s_size, svg_cds);
  }
  d3.select("[id=cds]")
  .attr("transform",'translate(30,0)')
}

//----------------------AXIS----------------------------

function axis(start, s_size){
  stop = start+s_size-1;
  
  var xscale = d3.scaleLinear()
    .domain([start, stop])
    .rangeRound([0, width-60]); // rangeRound makes sure there's no decimals ?
    //.range([0, width-60]);

  let t = (stop-start)/5;
var x_axis = d3.axisBottom()
        .tickFormat(d3.format("d")) // pas de virgule pour les milliers
        .tickValues(d3.range(start,stop+1,((stop-start)/5)))
        //.tickValues([start, Math.round((start+t)/1000)*1000, Math.round((start+2*t)/1000)*1000 , Math.round((start+3*t)/1000)*1000, Math.round((start+4*t)/1000)*1000,stop+1])
        //.ticks(5) // nombre de graduation sur l'axe
        .scale(xscale);
    
  d3.select("#genomic_ax").remove();
  var svg_grad = svg.append("g").attr("id", "genomic_ax")
            .attr("transform", "translate(30, " + 30  +")")
            .call(x_axis)
}

//--------------------PREVIOUS AXIS---------------------

function axis_graduation(x0, x1) {

    let xstep_10 = Math.pow(10, Math.floor(Math.log10(x1 - x0)));
    let nticks_10_mean = (x1 - x0 + 1) / xstep_10;
    let nticks_target = 5;
    let adj_fact = [2, 1, 0.5, 0.2];
    let adj_ichoose_ref = 10000000;
    let adj_ichoose = 0;
  
    for ( let i = 0 ; i < adj_fact.length ; i++ ) {
  
      let tmp = Math.abs((nticks_10_mean / adj_fact[i]) - nticks_target);
  
      if ( tmp < adj_ichoose_ref ) {
        adj_ichoose_ref = tmp;
        adj_ichoose = i;
      }
    }
  
    let xstep_adj = xstep_10 * adj_fact[adj_ichoose];
    let xtick0_adj = Math.ceil(x0 / xstep_adj) * xstep_adj;
    let nintervals_adj = Math.floor((x1 - xtick0_adj) / xstep_adj);
  
    let txticks = [];
  
    // 1st position
    txticks.push(x0);
  
    for ( let i = 0; i <= nintervals_adj; i++ ) {
      txticks.push((xtick0_adj + i * xstep_adj));
    }
  
    if ( txticks[nintervals_adj + 1] != x1 )	{ txticks.push( x1); }
  
    return txticks;
}

function genomic_axis(start, nb_pb, width, svg) {

    // Graduations
    let grad = axis_graduation(start, (start+nb_pb-1));
    let y = 20;
    // Axis
    svg.append("line")
     .attr("x1", 0)
     .attr("y1", y)
     .attr("x2", width_svg)
     .attr("y2", y)
     .style("stroke", "rgb(0,0,0)")
     .style("stroke-width", 1);
  
    // Graduations
    for ( let i = 0 ; i < grad.length ; i++) {
  
      let w_size = width_svg;
      let x = ((grad[i] - start) * w_size) / nb_pb;
  
      let g_size = w_size / nb_pb;
      if ( Math.trunc(g_size) > 0 ) {
        svg.append("rect")
           .attr("x", x)
           .attr("y", y)
           .attr("width", g_size)
           .attr("height", 4);
      }
      else {
        svg.append("line")
         .attr("x1", x)
         .attr("y1", y)
         .attr("x2", x)
         .attr("y2", y+5)
         .style("stroke", "rgb(0,0,0)")
         .style("stroke-width", 1);
      }
  
      let txt_grad = Math.ceil(grad[i]).toString();
      let units = svg.append("text");
      units.attr("x", x-(txt_grad.length * 3) + g_size/2 )
           .attr("y", y+20)
           .style("fill", "rgb(0,0,0)")
           .attr("font-size", "13");
      units.text(txt_grad);
    }
}

function get_axis(d_start, s_size, width) {
      d3.select("#genomic_axis").remove();
      var g_axis = svg.append("g").attr("id", "genomic_axis");
      genomic_axis(d_start, s_size, width, g_axis);
}

//-------------------FORMES VARIÉES --------------------


function rectangle(start, stop, svg_rect){
  let width_r = (stop - start);
  //width_r = width_r* (width_svg/(s_size-1));
  let r_svg = svg_rect.append("rect")
                        .attr("x", start)
                        .attr("y", 0)
                        .attr("width", width_r)
                        .attr("height", height)
                        .style("fill", background)
}

function cds(cds, seq_start, seq_stop, svg_cds){
  let startY=120
  let startX = cds.start *(width_svg/(s_size-1));
  let stopX = cds.stop *(width_svg/(s_size-1));
  //let length = stopX - startX
  let coord = "";

  //pas de CDS < 5 pour le moment
  //que sens +
  coord += (startX)+","+(startY+20)+" ";
  coord += (startX)+","+(startY+10)+" ";
  coord += (stopX-5)+","+(startY+10)+" ";
  coord += (stopX-5)+","+(startY+5)+" ";
  coord += (stopX)+","+(startY+15)+" ";
  coord += (stopX-5)+","+(startY+25)+" ";
  coord += (stopX-5)+","+(startY+20);
  
  
  let g_feat = svg_cds.append("g").attr("id", "cds_"+cds.id);

  var name = g_feat.append("text");
  let y_name = 102;
  name.attr("x", startX+5)
      .attr("y", y_name)
      .attr("class", "name")
      .attr("id", cds.id)
      .style("fill", cds_color)
      .attr("visibility", "hidden")
      .attr("font-size", "13")
      .text(cds.id);

  g_feat.append("polygon")
      .attr("points", coord)
      .attr("id", "cds_"+cds.id)
      .on("click", function() { click(cds, seqlen); })
      .on("mouseover", function() { over(name, g_feat); })
      .on("mouseout", function() { out(name, g_feat, cds); });

  return coord;
}

//---------------------EVENTS----------------------------

var zoom = 1; //zoom
var decalage = s_size/2;
var conversion = (width_svg/(s_size-1))
var l_start = 1;

//------------------------ZOOM-----------------------

document.getElementById("zoom_small_in").onclick = function(){
  if(s_size*0.75 < 10){move = 10/(s_size-1);}
  else{ move = 0.75}

  zoom /= move;
  s_size = Math.floor(s_size*move);

  change_svg(l_start,zoom,s_size);
      
}

document.getElementById("zoom_small_out").onclick = function(){

  if(Math.floor(s_size*1.5) <= seqlen){ // dézoom possible
    zoom/= 1.5;
    s_size = Math.floor(s_size*1.5);

    if(l_start+s_size-1 > seqlen){  //décaler le start   
      move = l_start - seqlen-s_size+1;
      l_start= seqlen-s_size+1;
    }
  }
  else{ //dézoom trop puissant
    zoom=1;
    s_size =seqlen;
    l_start=1;
  }
  
  change_svg(l_start,zoom,s_size);
  
}

document.getElementById("zoom_in").onclick = function(){
  move=2;
  if(s_size/2 < 10){move = s_size/10;}

  zoom *= move;
  s_size = Math.floor(s_size/move);


  change_svg(l_start,zoom,s_size);
    
}

document.getElementById("zoom_out").onclick = function(){
  move=2;

  if(Math.floor(s_size*move) <= seqlen){ // dézoom possible
    zoom/= move;
    s_size = Math.floor(s_size*move);
    if(l_start+s_size-1 > seqlen){ //décaler le start
      move = l_start - seqlen-s_size+1;
      l_start= seqlen-s_size+1;
    }
  }
  else{ //dézoom trop puissant
    zoom=1;
    s_size =seqlen;
    l_start=1;
  }


  change_svg(l_start,zoom,s_size);

}

//-----------------Neutral ZOOM-----------------

document.getElementById("zoom_neutral").onclick = function(){
  s_size = 10000;
  zoom=1;

  change_svg(l_start,zoom,s_size);
  
}

//----------------DECALAGE---------------------
document.getElementById("small_left").onclick = function(){ 
   
  if((l_start-decalage) < 1){ move = l_start-1;}
  else{ move = decalage}

  l_start-=move;


  change_svg(l_start,zoom,s_size);
  
}

document.getElementById("small_right").onclick = function() {

  if((l_start+s_size+decalage-1) >= seqlen){ move = seqlen-(l_start+s_size-1);}
  else{ move = decalage}

  l_start+=move;


  change_svg(l_start,zoom,s_size);
}

document.getElementById("big_left").onclick = function(){
  
  if((l_start-2*decalage) < 1){ move = l_start-1;}
  else{ move = 2*decalage}

  l_start-=move;


  change_svg(l_start,zoom,s_size);
}

document.getElementById("big_right").onclick = function() {

  if((l_start+s_size+2*decalage-1) >= seqlen){ move = seqlen-(l_start+s_size-1);}
  else{ move = 2*decalage}

  l_start+=move;

  change_svg(l_start,zoom, s_size);
  
}
            
//--------VERIFICATION START ET STOP-----------
function check_size(l_size) {
  if ( l_size < 10 )            { l_size = 10; }
  else if ( l_size > seqlen )   { l_size = seqlen; }
  return l_size;
}

function check_start(l_start, start) {
  if ( l_start <= 0 )           { return(-start+1); } //start=1
  //else if ( start >= seqlen ) { return(-(start-seqlen - s_size + 1));}
  return -4;
}


//--------MOUSE CLICK--------------------------
let g_name = genome_name;
// Mouse click event
function click(cds, seq_size) {
  location.assign("/sp/"+g_name+"/"+cds.id +'/');
  //location.assign("/results/?id="+cds.name+"&size="+seq_size);
}

// Mouse over event
function over(name, f_feat) {

  name.attr("visibility","visible");
  name.style("fill", over_color);
  f_feat.style("fill", over_color);

}

// Mouse out event
function out(name, f_feat, cds) {
  
    name.attr("visibility","hidden");
    name.style("fill", cds_color);
    f_feat.style("fill", cds_color);
}


//---------------------------------------------
function change_svg(l_start, zoom, s_size){
  d3.select("[id=rectangle]").remove();
  var svg_rect = svg.append("g").attr("id", "rectangle");
  rectangle(0,30, svg_rect);
  rectangle(width-30,width, svg_rect);

  axis(l_start, s_size);
  
  position=-l_start*(width_svg/(s_size-1));

 d3.select("[id=cds]")
 .attr("transform", "translate("+ (position+30) +",0), scale(+"+ zoom +",1)")
}

function check_cds(cds, coord, l_start, s_size){
  // let seq_stop = l_start+s_size-1;
  // //start out
  // if(cds.stop < l_start){
    
  // }
  // //stop out
  // if(cds.start > seq_stop){

  // }
  d3.select("[id=cds_first]")
      .style("fill", "green")
      .attr("points", coord);
}
