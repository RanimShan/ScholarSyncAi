const express = require('express');
const app = express();

// Default to the environment's PORT or 10000 if not set
const PORT = process.env.PORT || 10000;  

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
