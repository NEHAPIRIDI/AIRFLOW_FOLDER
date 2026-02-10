import { Line } from "react-chartjs-2";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

export default function Charts(){

  const data = {
    labels:["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    datasets:[
      {
        label:"DAG Runs",
        data:[12,15,9,18,20,17,22],
        borderColor:"#6366f1",
        tension:0.3
      }
    ]
  };

  return <Line data={data}/>;
}
