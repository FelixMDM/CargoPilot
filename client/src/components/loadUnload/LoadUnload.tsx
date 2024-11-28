
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
            <div className="flex flex-row w-full bg-slate-100 space-x-2 text-xl">
                <div className="text-black bg-slate-400 rounded-2xl m-2 p-4 cursor-pointer hover:text-white">
                    Load
                </div>
                <div className="text-black bg-slate-400 rounded-2xl m-2 p-4 cursor-pointer hover:text-white">
                    Unload
                </div>
            </div>
            <div className="flex flex-col w-[80%] items-center border-2 border-slate-400">
                <div className="w-full grid grid-cols-12 grid-rows-8 gap-4 m-3 text-center">
                    {Array.from({ length: 96 }).map((_, index: number) => (
                        <div key={index} className="cell m-auto">
                            {String(index % 12 + 1)}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default LoadUnload;