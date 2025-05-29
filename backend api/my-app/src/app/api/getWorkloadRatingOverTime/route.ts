import { NextResponse } from 'next/server';

export async function GET(request: Request) 
{
    try
    {
        const { searchParams } = new URL(request.url);
        const courseId = searchParams.get('courseId');
        const semestersBack = parseInt(searchParams.get('semestersBack') || '2')

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

        if (courseId == "EN.601.461" && semestersBack == 4)
        {
            return NextResponse.json(
                { 
                    FA2022 : 3.24,
                    FA2021 : 3.82,
                    FA2020 : 4.05,
                    SP2020 : 3.66
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