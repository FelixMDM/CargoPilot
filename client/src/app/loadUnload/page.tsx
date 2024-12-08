import ContainersPanel from "@/components/containers/ContainersPanel";
import LoadUnload from "@/components/loadUnload/LoadUnload";

const page = () => {
    return (
        <div>
            <LoadUnload />
            <ContainersPanel />
        </div>
    );
}

export default page;
