import Joi from 'joi';

export const queryUsersSchema = Joi.object({
  Name: Joi.string().optional(),
  Email: Joi.string().email().optional(),
}).or('Name', 'Email');
