#ifndef STACK_H_INCLUDED
#define STACK_H_INCLUDED



typedef struct my_snode
{
    struct btnode* data;
    struct my_snode *next;

}SNO;

void init(SNO *top);
void push(SNO *top,struct btnode* x);
struct btnode* pop(SNO* top);

//#else

#define N 30

typedef struct my_stack
{
    struct btnode* v[N];
    int top;
}STA;

void init(STA *s);
void push(STA *s,struct btnode* x);
struct btnode* pop(STA *s);



#endif // STACK_H_INCLUDED
