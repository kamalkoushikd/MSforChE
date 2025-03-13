function createLineChart({ 
    elementId, 
    data, 
    width = 600, 
    height = 400, 
    title = "Line Chart",
    labelColor = "#000000", 
    lineColor = "steelblue"
}) {
    if (!data || data.length === 0) {
        console.error("No data available for the chart.");
        return;
    }

    console.log("Rendering chart in:", elementId);

    const margin = { top: 60, right: 30, bottom: 60, left: 70 };

    const x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.x))
        .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
        .domain(d3.extent(data, d => d.y))
        .range([height - margin.bottom, margin.top]);

    const line = d3.line()
        .x(d => x(d.x))
        .y(d => y(d.y));

    const container = d3.select(`#${elementId}`);
    if (container.empty()) {
        console.error("Container element not found:", elementId);
        return;
    }

    container.selectAll("*").remove();

    const svg = container.append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("background-color", "#fff") 
        .style("color", labelColor)
        .style("border-radius", "15px");

    // Title
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", 30)
        .attr("fill", labelColor)
        .attr("text-anchor", "middle")
        .attr("font-size", "18px")
        .attr("font-weight", "bold")
        .style("fill","black")
        .text(title);

    // Grid lines
    svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x)
            .tickSize(-height + margin.top + margin.bottom)
            .tickFormat("")
        )
        .style("color", "#ddd");

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y)
            .tickSize(-width + margin.left + margin.right)
            .tickFormat("")
        )
        .style("color", "#ddd");

    // Path setup (animation not triggered yet)
    const path = svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", lineColor)
        .attr("stroke-width", 2)
        .attr("d", line);

    const totalLength = path.node().getTotalLength();

    path.attr("stroke-dasharray", `${totalLength} ${totalLength}`)
        .attr("stroke-dashoffset", totalLength);

    // Axis
    svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x))
        .selectAll("text")  
        .style("fill", "black");

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .selectAll("text")  
        .style("fill", "black");

    // Axis labels
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", height - 20)
        .attr("text-anchor", "middle")
        .attr("font-size", "14px")
        .style("fill", "black")
        .text("2θ (degrees)");

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", 20)
        .attr("text-anchor", "middle")
        .attr("font-size", "14px") 
        .style("fill", "black")
        .text("Intensity (a.u.)");

    // Legend
    const legend = svg.append("g")
        .attr("transform", `translate(${width - 150}, ${margin.top - 20})`);

    legend.append("rect")
        .attr("width", 12)
        .attr("height", 12)
        .attr("font-size", 10)
        .style("fill", lineColor);
    
    const legendbox = "X-Ray Diffraction";
    legend.append("text")
        .attr("x", 20)
        .attr("y", 10)
        .attr("font-size", 12)
        .style("fill", "black")
        .text(legendbox);
    // ✅ Trigger animation when graph enters viewport
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Start line animation
                path.transition()
                    .duration(2000)
                    .ease(d3.easeCubicOut)
                    .attr("stroke-dashoffset", 0);

                // Stop observing after first trigger
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 }); // Trigger at 50% visibility

    observer.observe(container.node());
}
