// frontend/src/GraphView.js
import React, { useEffect, useState } from 'react';
import { ForceGraph2D } from 'react-force-graph';


function GraphView() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/graph')
      .then(res => res.json())
      .then(data => {
        const nodesSet = new Map();
        const links = data.graph.map(link => {
          nodesSet.set(link.source, { id: link.source, label: link.source_summary });
          nodesSet.set(link.target, { id: link.target, label: link.target_summary });
          return { source: link.source, target: link.target };
        });
        setGraphData({ nodes: Array.from(nodesSet.values()), links });
      });
  }, []);

  return (
    <div style={{ height: '600px', background: '#000' }}>
      <ForceGraph2D
        graphData={graphData}
        nodeLabel="label"
        nodeAutoColorBy="id"
        linkDirectionalParticles={2}
      />
    </div>
  );
}

export default GraphView;
