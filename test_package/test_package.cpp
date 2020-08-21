#include <aws/lambda-runtime/runtime.h>

using namespace aws::lambda_runtime;

static invocation_response my_handler(invocation_request const &req)
{
    return invocation_response::failure("error message here",
                                        "error type here");
}

int main()
{
    run_handler(my_handler);
    return 0;
}
