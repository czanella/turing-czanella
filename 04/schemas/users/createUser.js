import Joi from 'joi';

export const createUserSchema = Joi.object({
  Id: Joi.string().required(),
  Name: Joi.string().required(),
  Email: Joi.string().email().required(),
});
