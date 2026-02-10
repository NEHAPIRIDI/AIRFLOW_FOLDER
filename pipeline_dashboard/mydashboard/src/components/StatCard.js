import { Card, CardContent, Typography } from "@mui/material";

export default function StatCard({title, value, subtitle}) {

  return (
    <Card sx={{ minWidth: 200, borderRadius: 3 }}>

      <CardContent>

        <Typography variant="subtitle2">{title}</Typography>

        <Typography variant="h4" fontWeight="bold">
          {value}
        </Typography>

        <Typography color="green">
          {subtitle}
        </Typography>

      </CardContent>

    </Card>
  );
}
