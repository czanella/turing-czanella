import express from 'express';
import { userRoutes } from './routes/users.js';

const app = express();
const port = parseInt(process.env.PORT ?? '3000');

app.use('/users', userRoutes);

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
