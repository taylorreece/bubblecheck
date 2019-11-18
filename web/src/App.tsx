import {CssBaseline} from "@material-ui/core";
import React from "react";
import BCDrawer from "./components/BCDrawer";
import BCNavBar from "./components/BCNavBar";
import {AuthProvider} from "./contexts/AuthContext";

class App extends React.Component {
  public render() {
    return (
      <React.Fragment>
        <AuthProvider>
          <div>
            <CssBaseline />
            <BCNavBar />
            <BCDrawer />
          </div>
        </AuthProvider>
      </React.Fragment>
    );
  }
}

export default App;
