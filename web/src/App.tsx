import {Button} from "@material-ui/core";
import React from "react";
import {AuthConsumer, AuthProvider} from "./contexts/AuthContext";

function PrintUserInfo(props: any) {
  return (
    <div>
      User Id: {props.user.usersid} <br />
      Email: {props.user.email} <br />
      Teacher Name: {props.user.teacher_name} <br />
    </div>
  );
}

const App: React.FC = () => {
  return (
    <div>
      <Button variant="contained" color="primary" href="/api/users/oauth/cognito/login">Login</Button>
      <Button variant="contained" color="secondary" href="/api/users/logout">Logout</Button>
      <AuthProvider>
        <AuthConsumer>
          {(authctx) => <PrintUserInfo user={authctx.user} />}

        </AuthConsumer>
      </AuthProvider>
    </div>
  );
};

export default App;
