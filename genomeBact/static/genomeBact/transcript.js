var width = 1200;
var height = 400;
s_size = 10000;
var width_svg = 1200-60;

var fenetre= d3.select("#svg_genomic_view").append("svg")
              .attr("width", width)
              .attr("height", height)
              .attr("id", "fenetre")
              .style("background", "lightgray")
              ;
var svg = d3.select("#svg_g").append("svg")
              .attr("width", width_svg)
              .attr("height", height-90)
              .attr("id", "svg")
              .style("background", "#C1E1C1")
              ;

genomic_view(s_size);
function genomic_view(s_size){
  
  get_axis(0, s_size+1, width);
  axis(0, s_size);
  fleche();
  ellipse(2000,4000,0);

  var svg_triangle = svg.append("g").attr("id", "triangle");
  triangle(4000,6000,1, svg_triangle);
  triangle(500,2000,-1, svg_triangle);

  var svg_rect = svg.append("g").attr("id", "rectangle");
  rectangle(0,100,0, svg_rect);
  rectangle(2000,4000,0, svg_rect);
  rectangle(8000,9900,0, svg_rect);

}

function changeColor(){
  d3.selectAll("rect")
    .style("fill", "pink");
}

//----------------------AXIS----------------------------

function axis(start, stop){
  var xscale = d3.scaleLinear()
    .domain([start, stop])
    .rangeRound([0, width-60]); // rangeRound makes sure there's no decimals ?
    //.range([0, width-60]);

var x_axis = d3.axisBottom()
        .tickFormat(d3.format("d")) // pas de virgule pour les milliers
       // .tickValues(d3.range(start,stop+1,((stop-start)/5)))
        .tickValues([0,2000,4000,6000,10000])
        //.ticks(5) // nombre de graduation sur l'axe mais must be div by 2, 5 or 10
        .scale(xscale);
    
  d3.select("#genomic_ax").remove();
  var svg_grad = fenetre.append("g").attr("id", "genomic_ax")
            .attr("transform", "translate(30, " + 60  +")")
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
  
    // Axis
    svg.append("line")
     .attr("x1", 0)
     .attr("y1", 20)
     .attr("x2", width_svg)
     .attr("y2", 20)
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
           .attr("y", 20)
           .attr("width", g_size)
           .attr("height", 4);
      }
      else {
        svg.append("line")
         .attr("x1", x)
         .attr("y1", 20)
         .attr("x2", x)
         .attr("y2", 20+5)
         .style("stroke", "rgb(0,0,0)")
         .style("stroke-width", 1);
      }
  
      let txt_grad = Math.ceil(grad[i]).toString();
      let units = svg.append("text");
      units.attr("x", x-(txt_grad.length * 3) + g_size/2 )
           .attr("y", 40)
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

function fleche(){
  d3.select("#fleche").remove();
  var svg_fleche = svg.append("g").attr("id", "fleche");

  svg_fleche.append("polygon")
            .attr("points", "76.626,120 76.626,110 224.386,110 224.386,105 229.386,115 224.386,125 224.386,120")
            .style("fill", "rgb(30, 183, 210)");
}

function rectangle(start, stop, sens, svg_rect){
  //d3.select("#rect").remove();
  let width_r = (stop - start);
  width_r = width_r* (width_svg/s_size);
  r_svg = svg_rect.append("rect")
                        .attr("x", start*(width_svg/s_size))
                        .attr("y", 50)
                        .attr("width", width_r)
                        .attr("height", 25)
                        .style("fill", 'lightblue')
}

function ellipse(start, stop, sens){
  d3.select("#ellipse").remove();
  var svg_ellipse = svg.append("g").attr("id", "ellipse");
  
  let width_e = (stop - start);
  width_e = width_e* (width_svg/s_size);

  svg_ellipse.append("ellipse")
              .attr("cx", (start*((width_svg)/s_size) + width_e/2))
              .attr("cy", 200)
              .attr("rx", width_e/2)
              .attr("ry", 12.5)
              .style("fill", "rgb(255, 0, 0)")
}

function triangle(start, stop, sens, svg_triangle){
  if(sens == -1){
    start = s_size -start;
    stop = s_size - stop;
  }

  let width_t = (stop - start);
  width_t = width_t* (width_svg/s_size);

  let end = start*((width_svg)/s_size);
  svg_triangle.append("polygon")
              .attr("points","" + (end+width_t) + ",270 "+ end +",260 "+ end +",280")
              .style("fill", "yellow");

}

//---------------------EVENTS----------------------------

var zoom = 1; //zoom
var step = 2;
var position = 0; //décalage du svg

var actual_start = 0;
var actual_stop = s_size;

function zoom_in(){
    zoom *= step;
    actual_stop /=step;
    axis(actual_start, actual_stop);
 
    d3.select("[id=rectangle]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")
  
    d3.select("[id=fleche]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=ellipse]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=triangle]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")
   
    d3.select("[id=genomic_axis]")
      .attr("transform", "translate("+ (position) +",0), scale(+"+ zoom +",1)")
      
}

function zoom_out(){
  // if(actual_start>0 && actual_stop*step >= s_size+actual_start ){ //si en dézoomant on sort du cadre mais que c'est dû à un décalage du start
  //   actual_start-=decalage;
  //   actual_stop-=decalage;
  // }
  if((actual_stop*step <= s_size)){ // en dézoomant on ne dépasse pas l'axe initial
    zoom/=step;

    actual_stop *=step;
    axis(actual_start, actual_stop);

    d3.select("[id=rectangle]")
      .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)");

    d3.select("[id=fleche]")
      .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)");

    d3.select("[id=ellipse]")
      .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)");

    d3.select("[id=triangle]")
      .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)");
    
    d3.select("[id=genomic_axis]")
      .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)");
  }
  else if(actual_start == 0){
    actual_stop = s_size;
    zoom = 1;
    axis(actual_start, actual_stop);

    d3.select("[id=rectangle]")
      .attr("transform", "scale(+"+ zoom +",1)");

    d3.select("[id=fleche]")
      .attr("transform", "scale(+"+ zoom +",1)");

    d3.select("[id=ellipse]")
      .attr("transform", "scale(+"+ zoom +",1)");

    d3.select("[id=triangle]")
      .attr("transform", "scale(+"+ zoom +",1)");

      d3.select("[id=genomic_axis]")
      .attr("transform", "scale(+"+ zoom +",1)");
  }
}

var move = 0;
var decalage =100;

function left(){
  if( actual_start-decalage >=0){
    
    move+=decalage*(width_svg/s_size)*zoom;
    position=move;

    actual_start-=decalage;
    actual_stop-=decalage;
    axis(actual_start, actual_stop);

    d3.select("[id=rectangle]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=fleche]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=ellipse]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=triangle]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")
   
    d3.select("[id=genomic_axis]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")
  }
}

function right(){
  if( actual_stop+decalage <= s_size){
    move-=decalage*(width_svg/s_size)*zoom;
    position=move;

    actual_start+=decalage;
    actual_stop+=decalage;
    axis(actual_start, actual_stop);

    d3.select("[id=rectangle]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=fleche]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=ellipse]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=triangle]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")

    d3.select("[id=genomic_axis]")
    .attr("transform", "translate("+ position +",0), scale(+"+ zoom +",1)")
  
  }
  
}

            