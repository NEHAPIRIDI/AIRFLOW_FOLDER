import { AppBar, Toolbar, Typography, Button, Chip, Box } from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";

export default function Topbar({ onRefresh }) {

  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        background: "white",
        color: "black",
        borderRadius: 2,
        mb: 3
      }}
    >

      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between"
        }}
      >

        {/* Left Title */}
        <Typography variant="h6" fontWeight="bold">
          Dashboard Overview
        </Typography>


        {/* Right Controls */}
        <Box>

          <Button
            variant="contained"
            startIcon={<RefreshIcon />}
            sx={{ mr: 2 }}
            onClick={onRefresh}
          >
            Refresh Now
          </Button>

          <Chip
            label="All Systems Operational"
            color="success"
            variant="filled"
          />

        </Box>

      </Toolbar>

    </AppBar>
  );
}
