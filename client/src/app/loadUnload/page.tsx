"use client";

import React, {useState} from "react";
import { SelectedCellsProvider } from "../../components/loadUnload/SelectedCellsContext";
import Unload from "../../components/loadUnload/Unload";
import Steps from "../../components/loadUnload/Steps";

const App = () => {
  const [currScreen, setCurrScreen] = useState("unload");

  const handleScreenSteps = () => {
    setCurrScreen("steps")
  }
  return (
    <SelectedCellsProvider>
      {currScreen == "unload" ? (
      <Unload nextStepsPage={handleScreenSteps}/>
      ) : (
        <Steps />
      )}
    </SelectedCellsProvider>
  );
};

export default App;
