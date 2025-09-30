// THIS IS AN EXAMPLE ROUTE

import { NextResponse } from 'next/server';

export async function GET(request: Request) 
{
    try
    {
        const { searchParams } = new URL(request.url);
        const courseId = searchParams.get('courseId');

        if (!courseId) 
            {
            return NextResponse.json(
                { 
                    error: 'Course ID is required'
                },
                {
                    status: 400
                }
            );
        }

        if (courseId == "EN.601.461")
        {
            return NextResponse.json(
                { 
                    rating: 3.76
                }
            );
        }

        return NextResponse.json(
            { 
                rating: -1
            }
        );
    } 
    catch (error) 
    {
        return NextResponse.json(
            { 
                error: 'Failed to get workload rating'
            },
            {
                status: 500 
            }
        );
    }
} 