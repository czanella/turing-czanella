const users = {};

export const addUser = ({ Id, Name, Email }) => users[Id] = { Id, Name, Email };

export const removeUser = ({ Id }) => {
  if (!(Id in users)) {
    return false;
  }

  delete users[Id];

  return true;
}

export const getUser = ({ Id }) => users[Id] ?? null;

export const queryUser = ({ Name, Email }) =>
  Object.values(users)
    .filter(user =>
      (!Name || user.Name === Name) &&
      (!Email || user.Email === email)
    );
