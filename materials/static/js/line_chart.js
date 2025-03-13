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

    const container = d3.select(`#${elementId}`)
        .style("position", "relative")
        .style("display", "block")
        .style("margin", "0 auto")
        .attr("class", "center container justify-content-center");
    if (container.empty()) {
        console.error("Container element not found:", elementId);
        return;
    }
    
    // Ensure container is relatively positioned for proper tooltip placement

    // Clear previous content
    container.selectAll("*").remove();

    // Create SVG first
    const svg = container.append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("background-color", "#181A1B")
        .style("color", labelColor)
        .style("border-radius", "15px");

    // Create tooltip (appended to container)
    const tooltip = container.append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("display", "none")
        .style("background", "rgba(255, 255, 255, 1)")
        .style("padding", "5px")
        .style("border", "1px solid #ccc")
        .style("border-radius", "3px")
        .style("color", "black")

    // Scales
    const x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.x))
        .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
        .domain(d3.extent(data, d => d.y))
        .range([height - margin.bottom, margin.top]);

    // Line generator
    const line = d3.line()
        .x(d => x(d.x))
        .y(d => y(d.y));

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

    // Draw line path
    const path = svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", lineColor)
        .attr("stroke-width", 2)
        .attr("d", line);

    const totalLength = path.node().getTotalLength();

    path.attr("stroke-dasharray", `${totalLength} ${totalLength}`)
        .attr("stroke-dashoffset", totalLength);

    // Draw axes
    svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .style("fill", "white");

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .selectAll("text")
        .style("fill", "white");

    // Title
    

    // Axis labels
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", height - 20)
        .attr("text-anchor", "middle")
        .attr("font-size", "14px")
        .style("fill", "white")
        .text("2θ (degrees)");

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", 20)
        .attr("text-anchor", "middle")
        .attr("font-size", "14px")
        .style("fill", "white")
        .text("Intensity (a.u.)");

    // Interactive circle for tooltip display
    const circle = svg.append("circle")
        .attr("r", 0)
        .attr("fill", lineColor)
        .style("stroke", "white")
        .attr("opacity", 0.9)
        .style("pointer-events", "none");

    // Listening rectangle for mouse events
    const listeningRect = svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all");

    listeningRect.on("mousemove", function (event) {
        const [xCoord] = d3.pointer(event, this);
        const bisectX = d3.bisector(d => d.x).left;
        const x0 = x.invert(xCoord);
        let i = bisectX(data, x0, 1);

        // Safeguard for edge cases
        if (i >= data.length) i = data.length - 1;

        const d0 = data[i - 1];
        const d1 = data[i];
        let dNearest;
        if (!d0) {
            dNearest = d1;
        } else if (!d1) {
            dNearest = d0;
        } else {
            dNearest = (x0 - d0.x) > (d1.x - x0) ? d1 : d0;
        }

        const xPos = x(dNearest.x);
        const yPos = y(dNearest.y);

        // Update circle position and radius
        circle.attr("cx", xPos)
              .attr("cy", yPos);

        circle.transition()
              .duration(50)
              .attr("r", 5);

        // Show and update tooltip content and position
        tooltip.style("display", "block")
               .style("left", `${xPos + 20}px`)
               .style("top", `${yPos + 20 }px`)
               .html(`<strong>Angle:</strong> ${dNearest.x.toFixed(5)}° <br><strong>Intensity:</strong> ${dNearest.y.toFixed(5)}(a.u.)`);
    });

    listeningRect.on("mouseleave", function () {
        circle.transition()
              .duration(50)
              .attr("r", 0);

        tooltip.style("display", "none");
    });

    // Trigger animation when graph enters the viewport
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                path.transition()
                    .duration(4000)
                    .ease(d3.easeCubicOut)
                    .attr("stroke-dashoffset", 0);

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    observer.observe(container.node());

    // Append legend AFTER interactive elements so it appears on top
    const legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${width - 175}, ${margin.top - 20})`);

    legend.append("rect")
        .attr("width", 12)
        .attr("height", 12)
        .style("fill", lineColor)
        .style("stroke", "white");

    legend.append("text")
        .attr("x", 20)
        .attr("y", 10)
        .attr("font-size", 12)
        .style("fill", "white")
        .text("X-Ray Diffraction");

    // Alternatively, if you need to raise an existing legend group:
    svg.select(".legend").raise();
    
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", 30)
        .attr("fill", labelColor)
        .attr("text-anchor", "middle")
        .attr("font-size", "18px")
        .attr("font-weight", "bold")
        .style("fill", "white")
        .text(title);
    
}
