#include <stdio.h>
#include <stdlib.h>
#include "mylib.h"
#include <string.h>

//*****************************Function
float square2(float a)
{
    printf("%d", external_func());
    return a * a;
}

int main()
{
    //*****************************base
    printf("hello\n");
    int a = 3;
    char myText[] = "Hello";
    float ff = 3.4;
    int fff = (int) ff;
    const int ad = 45;
    // scanf("%d", &a);
    // char fullName[30];
    // printf("Type your full name: \n");
    // fgets(fullName, sizeof(fullName), stdin);
    // printf("input was : %d \n", a);
    // %d or %i 	int 	
    // %f or %F 	float 	
    // %lf 	        double 	
    // %c 	        char 	
    // %s 	        string
    const int b = 2;
    #define C 3

    int g[4] = {56, 45, 213, 23};
    int h[2][3] = {{45, 46, 56}, {1, 2, 5}};

    //*****************************Loop if operator
    if (b == a)
    {
        printf("equal");
    }
    else
    {
        printf("not equal");
    }
    switch (a)
    {
    case 6:
        printf("b");
        break;
    case 5:
        printf("5");
        break;
    default:
        printf("else");
        break;
    }
    int count = 5;
    for (int i = 0; i < count; i++)
    {
        printf("%d", i);
    }
    while (count < 5)
    {
        if (count == 2)
        {
            continue;
        }
        printf("1");
        if (count == 3)
        {
            break;
        }
        count++;
    }
    do
    {
        count = 2;
        count++;
    } while (count < 5);

    //*****************************String
    char text1[] = "meysam";
    char text2[] = "ali";
    char text3[5];
    strcpy(text1, text3);
    printf("%d", strcmp(text1, text2));
    strcat(text1, text2);

    //*****************************macro
    #ifndef C
    #define C 10
    #endif

    #ifdef C2
    #undef C2
    #endif

    //if (1==2)
        //#error 1 not equal 2 ;
    
    //*****************************pointer

    float y = 2.23;
    float *x = &y;
    float z = *x;
    float const *hh = &y; // hh cant be changed
    const float *kk = &y; // y cant be changed
    const float const *ll = &y; // both y and ll cant be changed
    float **pp = &x; // two level pointer

    //*****************************struct
    struct student
    {
        int id;
        char name[10];
    };
    
    struct student s1 = {1,"meysam"};

    //*****************************file
    FILE *fptr;
    fptr = fopen("mylib.h", 'r'); // w,a,r
    char myString[100]; 
    fgets(myString, 100, fptr); 
    fclose(fptr);
    // fprintf(fptr, "Some text"); // Write some text to the file

    //*****************************enum
    enum Level {
        LOW,
        MEDIUM,
        HIGH
    };
    enum Level myVar = MEDIUM;
    printf("%d", myVar); // it will output 1, which represents MEDIUM

    return 0;
}