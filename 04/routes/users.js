import * as userService from '../services/users.js';
import express from 'express';
import { validationSchema } from '../middlewares/index.js';
import {
  createUserSchema,
  userEntitySchema,
  queryUsersSchema,
} from '../schemas/users/index.js';

export const userRoutes = express();

userRoutes.post('/',
  express.json(),
  validationSchema('body', createUserSchema),
  (req, res) => {
    const { Id, Name, Email } = req.body;
    const userExists = Boolean(userService.getUser({ Id }));

    userService.addUser({ Id, Name, Email });

    let status, message;
    if (userExists) {
      status = 200;
      message = `User ID ${Id} updated`;
    } else {
      status = 201;
      message = `User ID ${Id} created`;
    }
    res.status(status).json({ message });
  },
);

userRoutes.get('/query',
validationSchema('query', queryUsersSchema),
  (req, res) => {
    const { Name, Email } = req.query;

    const users = userService.queryUsers({ Name, Email });

    let status;
    if (users.length === 0) {
      status = 404;
    } else {
      status = 200;
    }

    res.status(status).json({ users });
  }
);

userRoutes.get('/:Id',
  validationSchema('params', userEntitySchema),
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

userRoutes.delete('/:Id',
  validationSchema('params', userEntitySchema),
  (req, res) => {
    const { Id } = req.params;
    const userExisted = userService.removeUser({ Id });

    let status, message;
    if (!userExisted) {
      status = 404;
      message = `User ID ${Id} not found`;
    } else {
      status = 200;
      message = `User ID ${Id} successfully removed`;
    }
    res.status(status).json({ message });
  }
);
