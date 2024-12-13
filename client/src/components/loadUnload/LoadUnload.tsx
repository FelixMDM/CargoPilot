
/**
 * 
 * I'm thinking that the best way to do this is gonna be yeah to map over a list of 96 to render all the grid boxes,
 * but functionally, later on down the line -> make an api call for the updated manifest/steps
 * 
 * Format is maybe a list (CSV?) of arrays [96 in len] that represent what box goes where? and each list entry is a step
 * or something close to that where only the colors are specified
 * 
 * Render the respective colors at each steps in that map loop that I have defined currently
 */

const LoadUnload = () => {
    return (
        <div className="flex flex-col font-archivo-narrow font-bold space-y-2 items-center">
            <div className="top-0 w-full bg-slate-100 font-archivo-narrow text-2xl font-bold z-40">
                <div className="flex justify-between items-center p-4">
                    <div className="text-black bg-slate-400 rounded-2xl p-4 m-2 hover:text-white">
                        Load
                    </div>
                    <div className="text-black bg-slate-400 rounded-2xl p-4 m-2 hover:text-white">
                        Unload
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoadUnload;