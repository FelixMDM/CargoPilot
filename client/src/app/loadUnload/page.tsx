import React from "react";
import { SelectedCellsProvider } from "../../components/loadUnload/SelectedCellsContext";
import Unload from "../../components/loadUnload/Unload";

const App = () => {
  return (
    <SelectedCellsProvider>
      <Unload />
    </SelectedCellsProvider>
  );
};

export default App;
