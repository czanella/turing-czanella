import Joi from 'joi';

export const userEntitySchema = Joi.object({
  Id: Joi.string().required(),
});
