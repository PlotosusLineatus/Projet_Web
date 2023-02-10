//     Copyright (C) 2020  Sandra Dérozier (INRAE)
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
let seq_start = urlParams.get('start');
let seq_size = urlParams.get('size');

let seqlen = length;

if(seq_start == null ){
  seq_start=1;
}
if(seq_size == null){
  seq_size=10000;
}
check_size(seq_size);
check_start(seq_start);

/*
// Size
if ( seq_size !== null ) {
  seq_size = check_size( parseInt(seq_size) );

  let url = location.href;
  url = url.toString().replace('size='+parseInt(seq_size).toString() , 'size=' + s_size.toString());
  history.replaceState(null,"", url);
}
else {
    seq_size = 10000;
}
*/

var width = 1200;
var height = 200;
var width_svg = 1200-60;
let background = "#FBF5F3"
let color = "#8DAA9D";
let over_color = "#45425A";
let list =list_cds;
let seq_stop = seq_start+seq_size-1;

/*
let seqlen = parseInt(sessionStorage.getItem("seqlen"));
let size = parseInt(sessionStorage.getItem("size"));
let l_start = parseInt(sessionStorage.getItem("start"));
let list = list_cds;
*/

var svg= d3.select("#svg_genomic_view").append("svg")
              .attr("width", width)
              .attr("height", height)
              .attr("id", "svg")
              .style("background", background);
              ;

genomic_view();
function genomic_view(){
  var svg_transcript = svg.append("g").attr("id", "transcript")
                    .style('fill', color)
                    ;

  get_axis(seq_start, seq_size, width); 
  d3.select("#genomic_axis").attr("transform",'translate(30,0)');  
 //CDS
 for(cds in list){
  draw_transcript(list[cds], seq_start, seq_stop, width_svg, 100, seq_size, svg_transcript);
 }
}

//-------------------- AXIS---------------------

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

//-------------------FORMES CDS --------------------

function draw_transcript(transcript, seq_start, seq_stop, w_size, startY, seq_size, g_transcript){
  let y = 0; //if ( transcript.complement == '-1' ) { y = 25; }
  let transcript_coord = {}; 
  transcript_coord["tail"]= 0;
  transcript_coord["tip"] = 0;

  let y_axis = new Array(5);
  y_axis[0]= startY+20+y;
  y_axis[1]=startY+10+y;
  y_axis[2]=startY+5+y;
  y_axis[3]=startY+15+y;
  y_axis[4]=startY+25+y;
  transcript_coord["y_axis"] = y_axis;
  transcript_coord["startY"] = startY +y;

  transcript["coord"] = transcript_coord;
  let g_feat = g_transcript.append("g").attr("id", "transcript_"+transcript.id);

  var points = g_feat.append("g").attr("id", "dots_"+transcript.id);

  // CDS name
  var name = g_feat.append("text");
  let y_name = startY+2+y; 
  //if ( transcript.complement == '-1' ) { y_name += 35; }
  name.attr("id", "name_"+transcript.id)
      .attr("y", y_name)
      .attr("class", "name")
      .style("fill", color)
      .attr("visibility", "hidden")
      .attr("font-size", "13")
      .text(transcript.id);

  // SVG writing
  var f_feat = g_feat.append("polygon").attr("id", transcript.id)
                     .style("fill", color)
                     .on("click", function() { click(transcript, seq_size); })
                     .on("mouseover", function() { over(name, f_feat, points); })
                     .on("mouseout", function() { out(transcript, name, f_feat, points); });

  check_transcript(transcript, seq_start, seq_size, width_svg);
  
}

function check_transcript(transcript, l_start, s_size, w_size){
  d3.select("#dots_l_"+transcript.id).remove();
  d3.select("#dots_r_"+transcript.id).remove();

  let seq_stop = l_start+s_size-1;
  let startX; let stopX =0;

  startX = ((transcript.start - l_start) * w_size) / (s_size-1);
  stopX = ((transcript.stop - l_start) * w_size) / (s_size-1);

  let s_length = stopX - startX;
  startX+=30;
  stopX+=30;
  //1st case: start & stop out (transcript hidden)
  if( (transcript.stop > seq_stop && transcript.start > seq_stop) ||  (transcript.stop <l_start && transcript.start < l_start)){
    transcript.coord["tail"]= -1;  
    transcript.coord["tip"] = -1;
    transcript.coord["middle"] = -1;
  }
  //2nd case: (transcript visible)
  else{
    //start in 
    if(transcript.start >= l_start && transcript.stop > l_start){
      transcript.coord["tail"]= startX;  
      if(transcript.start==seq_stop){
        transcript.coord["tail"] -=1; 
      }
    }
    //start out 
    if(transcript.start < l_start){
      transcript.coord["tail"] = 30;

      // Start points if start is out
      var points = d3.select("#dots_"+transcript.id);
      points.append("text").attr("id", "dots_l_"+transcript.id)
            .attr("x", 15)
            .attr("y", transcript.coord["startY"] +15)
            //.style("fill", transcript.new_color)
            .text("...");
  
    }
    //stop in 
    if(transcript.stop <= seq_stop && transcript.start < seq_stop) {
      transcript.coord["tip"] = stopX;
      
      if(transcript.stop==l_start){
        transcript.coord["tip"] = 1; 
      }
    }
    //stop out 
    if(transcript.stop > seq_stop){
      transcript.coord["tip"] = w_size+30;

      // Stop points if stop is out
      var points = d3.select("#dots_"+transcript.id);
      points.append("text").attr("id","dots_r_"+transcript.id)
            .attr("x", w_size + 35)
            .attr("y", transcript.coord["startY"] +15)
            //.style("fill", transcript.new_color)
            .text("...");
    }
  }
    
  var x = transcript.coord["tail"];
  s_length = transcript.coord["tip"] - transcript.coord["tail"];

  //SENS +
  if(transcript.stop > seq_stop){ // (real)tip out
      transcript.coord["middle"] = transcript.coord["tip"];
  }else{
      // Arrow
      if ( s_length >= 5 ) {
        transcript.coord["middle"] = transcript.coord["tip"]-5;
      }// Triangle
      else if(s_length == 5){
        transcript.coord["middle"] = transcript.coord["tail"];
      }//Rectangle
      else{
        transcript.coord["middle"] = transcript.coord["tip"];
      }
  }
  
  let y1_middle = transcript.coord["y_axis"][2];
  let y2_middle = transcript.coord["y_axis"][4];
  if( transcript.coord["middle"] == transcript.coord["tip"] ){
    y1_middle = transcript.coord["y_axis"][1];
    y2_middle = transcript.coord["y_axis"][0];
  }


  let coord = "";
  coord += transcript.coord["tail"]   +","+ transcript.coord["y_axis"][0]+" ";
  coord += transcript.coord["tail"]   +","+ transcript.coord["y_axis"][1]+" ";

  coord += transcript.coord["middle"] +","+ transcript.coord["y_axis"][1]+" ";
  coord += transcript.coord["middle"] +","+ y1_middle+" ";

  coord += transcript.coord["tip"]    +","+ transcript.coord["y_axis"][3]+" ";

  coord += transcript.coord["middle"] +","+ y2_middle+" ";
  coord += transcript.coord["middle"] +","+ transcript.coord["y_axis"][0];

  d3.select('#'+ transcript.id)
          .attr('points', coord);
  
  d3.select('#name_'+ transcript.id)
          .attr('x', x);
  
  d3.select('#dots_'+ transcript.id)
        .attr("stroke", color);
}

// Mouse click event
let g_name = genome_name;
function click(transcript, seq_size) {
  location.assign("/sp/"+g_name+"/"+transcript.id +'/');
}

// Mouse over event
function over(name, f_feat, points) {

  name.attr("visibility","visible");
  name.style("fill", over_color);
  f_feat.style("fill", over_color);
  if ( points != undefined ) {
    points.attr("stroke", over_color);
  }
}

// Mouse out event
function out(transcript, name, f_feat, points) {
  name.attr("visibility","hidden");
  name.style("fill", color);
  f_feat.style("fill", color);
  if ( points != undefined ) {
        points.attr("stroke", color);
  }
}

// Navigation buttons
document.getElementById("big_left").onclick = function(){
  if( seq_start != 1){
    seq_start = seq_start - size;
    seq_start = check_start(seq_start);

    let url = "/sp/"+g_name+"/?start="+seq_start+"&size="+seq_size;
    history.replaceState(null,"", url);
    resize_svg();
  }
}
document.getElementById("small_left").onclick = function(){
  if(seq_start != 1){
    seq_start = seq_start - seq_size/2;
    seq_start = check_start(seq_start);

    let url = "/sp/"+g_name+"/?start="+seq_start+"&size="+seq_size;
    
    history.replaceState(null,"", url);
    resize_svg();
  }
}
document.getElementById("big_right").onclick = function(){
  let seq_stop = seq_start+ seq_size-1;
  if(seq_stop != seqlen){
    seq_start = seq_start + seq_size;
    seq_start = check_start(seq_start);

    let url = "/sp/"+g_name+"/?start="+seq_start+"&size="+seq_size;
    history.replaceState(null,"", url);
    resize_svg();
  }
}
document.getElementById("small_right").onclick = function(){
  let seq_stop = seq_start+ seq_size-1;
  if(seq_stop != seqlen){
    seq_start = seq_start + seq_size/2;
    seq_start = check_start(seq_start);

    let url = "/sp/"+g_name+"/?start="+seq_start+"&size="+seq_size;

    history.replaceState(null,"", url);
    resize_svg();

  }
}

// Zoom buttons
document.getElementById("zoom_in").onclick = function(){
    seq_size = seq_size * 0.5;
    seq_size = check_size(seq_size);

    let url = "/sp/"+g_name+"/?"+"start="+seq_start+ "&size="+seq_size;

    history.replaceState( null,"", url);
    resize_svg();
}
document.getElementById("zoom_small_in").onclick = function(){
    seq_size = seq_size * 0.75;
    seq_size = check_size(seqlen);

    let url = "/sp/"+g_name+"/?"+"start="+seq_start+"&size="+seq_size;
    history.replaceState( null,"", url);
    resize_svg();
}
document.getElementById("zoom_neutral").onclick = function(){
  if(seq_size != 10000){
    let s_start = seq_start+ seq_size-1;
        
    seq_size = 10000;

    let url = "/sp/"+g_name+"/?"+"start="+seq_start+"&size="+seq_size;

    history.replaceState( null,"", url);
    resize_svg();
  }
}
document.getElementById("zoom_small_out").onclick = function(){
    let s_start = seq_start+ seq_size-1;
    seq_size = seq_size * 1.5;
    seq_size = check_size(seq_size);

    let url = "/sp/"+g_name+"/?"+"start="+seq_start+"&size="+seq_size;

    history.replaceState( null,"", url);
    resize_svg();
}
document.getElementById("zoom_out").onclick = function(){
    seq_size = seq_size * 2;
    seq_size = check_size(seq_size);

    let url = "/sp/"+g_name+"/?"+"start="+seq_start+"&size="+seq_size;

    history.replaceState( null,"", url);
    resize_svg();
}

function resize_svg(){

    get_axis(seq_start, seq_size, width);
    d3.select("#genomic_axis").attr("transform",'translate(30,0)');

    //CDS
    for(cds in list){
      check_transcript(list[cds], seq_start, seq_size, width_svg);
    }
}


function check_size(l_size) {
  if ( l_size < 10 )                     { l_size = 10; }
  else if ( l_size > seqlen )            { l_size = seqlen; }
  
  let l_start = seq_start;
  if ( (l_start + l_size-1) > seqlen )   { l_start = seqlen - l_size + 1;}
  seq_size=l_size;
  return l_size;
}

function check_start(start) {
  if ( start <= 0 )                     { start = 1; }
  else if ( start >= seqlen )           { start = seqlen - seq_size + 1; }
  if ( (start + seq_size-1) > seqlen )  { start = seqlen - seq_size + 1; }
  seq_start=start;
  return start;
}