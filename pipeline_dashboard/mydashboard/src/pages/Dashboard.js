import { Grid } from "@mui/material";
import { useEffect, useState } from "react";
import axios from "axios";

import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import Charts from "../components/Charts";
import Topbar from "../components/Topbar";

export default function Dashboard(){

  const [stats, setStats] = useState({
    total_dags: 0,
    active_dags: 0,
    running: 0,
    success_rate: 0
  });


  // Load real stats
  useEffect(() => {

    axios.get("http://localhost:8000/stats")
      .then(res => setStats(res.data))
      .catch(err => console.log(err));

  }, []);


  return (

    <div style={{ display:"flex" }}>

      <Sidebar/>

      <div style={{ flex:1, padding:"25px" }}>

        <Topbar onRefresh={() => window.location.reload()} />


        {/* STAT CARDS */}
        <Grid container spacing={2}>

          <Grid item>
            <StatCard
              title="Total DAGs"
              value={stats.total_dags}
              subtitle={`${stats.active_dags} Active`}
            />
          </Grid>

          <Grid item>
            <StatCard
              title="Success Rate"
              value={`${stats.success_rate}%`}
              subtitle="Last Runs"
            />
          </Grid>

          <Grid item>
            <StatCard
              title="Running"
              value={stats.running}
              subtitle="Live"
            />
          </Grid>

          <Grid item>
            <StatCard
              title="DQ Score"
              value="92%"
              subtitle="Excellent"
            />
          </Grid>

        </Grid>


        {/* CHART */}
        <div style={{ marginTop:"40px" }}>

          <h3>DAG Execution (Last 7 Days)</h3>

          <Charts/>

        </div>

      </div>

    </div>
  );
}
