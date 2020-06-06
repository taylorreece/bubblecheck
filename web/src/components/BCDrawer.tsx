import React from "react";
import { AuthConsumer } from "../contexts/AuthContext";

const myPage = (authctx: any) => {
  return (
    <div>
      <strong>Email:</strong> {authctx.user.email}
      <br />
      <strong>Name:</strong> {authctx.user.teacher_name}
      <br />
      <strong>UserID:</strong> {authctx.user.usersid}
      <br />
    </div>
  );
};

const BCDrawer: React.FC = () => {
  return (
    <div>
      <AuthConsumer>{(authctx) => myPage(authctx)}</AuthConsumer>
    </div>
  );
};

export default BCDrawer;
