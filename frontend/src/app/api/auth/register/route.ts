import { NextResponse } from "next/server";

export default async function POST(request: Request) {
    try {
        const {email, password} = await request.json();
        // validate email and password (email is valid and password is a certain number of characters)
        // try zod library
        console.log(email,password)
    } catch(e) {
        console.log("error",e)
    }

    return NextResponse.json({message:"success"})
}