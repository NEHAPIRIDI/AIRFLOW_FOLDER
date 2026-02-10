import { Drawer, List, ListItem, ListItemIcon, ListItemText } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import StorageIcon from "@mui/icons-material/Storage";
import BugReportIcon from "@mui/icons-material/BugReport";

export default function Sidebar() {

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 220,
        [`& .MuiDrawer-paper`]: { width: 220, background: "#0f172a", color: "white" }
      }}
    >
      <h3 style={{ textAlign: "center", padding: "10px" }}>ETL Hub</h3>

      <List>

        <ListItem button>
          <ListItemIcon><DashboardIcon style={{color:"white"}}/></ListItemIcon>
          <ListItemText primary="Overview"/>
        </ListItem>

        <ListItem button>
          <ListItemIcon><StorageIcon style={{color:"white"}}/></ListItemIcon>
          <ListItemText primary="DAGs"/>
        </ListItem>

        <ListItem button>
          <ListItemIcon><BugReportIcon style={{color:"white"}}/></ListItemIcon>
          <ListItemText primary="Logs"/>
        </ListItem>

      </List>
    </Drawer>
  );
}
