import * as userService from '../services/users.js';
import express from 'express';

export const userRoutes = express();

userRoutes.post('/',
  express.json(),
  (req, res) => {
    const { Id, Name, Email } = req.body;
    const message = userService.getUser({ Id }) ?
      `User ID ${Id} updated` :
      `User ID ${Id} created`;

    userService.addUser({ Id, Name, Email });

    res.json({ message });
  },
);

userRoutes.get('/:Id',
  (req, res) => {
    const { Id } = req.params;
    const user = userService.getUser({ Id });

    if (!user) {
      res.status(404).json({ message: `User ID ${Id} not found` });
    } else {
      res.json(user);
    }
  }
);
