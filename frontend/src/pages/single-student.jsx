import { useParams } from "react-router-dom"

export default function SingleStudent(){
    const {id} = useParams()


    return(
        <>user id: {id}</>
    )
}